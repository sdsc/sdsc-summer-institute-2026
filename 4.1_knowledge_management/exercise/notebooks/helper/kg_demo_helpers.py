from __future__ import annotations

import hashlib
import json
import os
import re
import textwrap
import uuid
from pathlib import Path
from typing import Any, Iterable, List

from pydantic import BaseModel, Field


class Entity(BaseModel):
    name: str = Field(description="The canonical entity name from the text.")
    type: str = Field(description="A short category such as Person, Organization, Place, Method, Dataset, or Concept.")
    description: str = Field(description="One sentence explaining what the entity is in this document.")
    evidence: str = Field(description="A short phrase or sentence copied from the source text that supports the extraction.")


class EntityExtraction(BaseModel):
    entities: List[Entity]


class Relationship(BaseModel):
    source: str = Field(description="The source entity name. It must match one extracted entity exactly.")
    target: str = Field(description="The target entity name. It must match one extracted entity exactly.")
    relationship: str = Field(description="A concise verb phrase such as USES, PRODUCES, LOCATED_IN, or COLLABORATES_WITH.")
    description: str = Field(description="One sentence explaining the relationship.")
    evidence: str = Field(description="A short phrase or sentence copied from the source text that supports the relationship.")


class RelationshipExtraction(BaseModel):
    relationships: List[Relationship]


class CorpusDocument(BaseModel):
    document_id: str
    source_name: str
    path: str
    text: str


class ChunkRecord(BaseModel):
    chunk_id: str
    document_id: str
    source_name: str
    chunk_index: int
    text: str


class ResolvedEntity(BaseModel):
    canonical_name: str
    type: str
    description: str = ""
    aliases: List[str] = Field(default_factory=list)
    source_names: List[str] = Field(default_factory=list)
    evidence: List[str] = Field(default_factory=list)


class ResolvedRelationship(BaseModel):
    source: str
    target: str
    relationship: str
    description: str = ""
    source_names: List[str] = Field(default_factory=list)
    evidence: List[str] = Field(default_factory=list)


SAMPLE_TEXT = """
SDSC runs a summer demo about drought planning in California.
Researchers use satellite imagery, river sensors, and climate reports to
understand water conditions. The Center for Hydrology shares sensor data with
SDSC. The demo shows how Weaviate stores OCR text chunks and Neo4j stores
entities and relationships. Students use the graph to answer questions about
organizations, datasets, and methods.
"""


DEMO_CORPUS_TEXTS: list[tuple[str, str]] = [
    (
        "01_drought_observations.pdf",
        """
        SDSC runs a summer demo about drought planning in California. Researchers
        use satellite imagery and river sensors to understand water conditions.
        The Center for Hydrology shares sensor data with SDSC for the workshop.
        """,
    ),
    (
        "02_remote_sensing_methods.pdf",
        """
        San Diego Supercomputer Center students compare Remote Sensing Imagery
        with seasonal climate outlooks. The knowledge graph links datasets,
        methods, and organizations that support drought planning.
        """,
    ),
    (
        "03_graph_vector_search.pdf",
        """
        The tutorial stores OCR text chunks in Weaviate for semantic search.
        Neo4j stores normalized entities and relationships. Students query the
        combined graph and vector representation from a Jupyter notebook.
        """,
    ),
]


def ensure_sample_pdf(pdf_path: str | Path = "data/sample_kg_note.pdf") -> Path:
    """Create a tiny sample PDF so the notebook can run without outside files."""
    path = Path(pdf_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return path
    _write_text_pdf(path, SAMPLE_TEXT)
    return path


def _write_text_pdf(path: Path, text: str) -> None:
    try:
        import fitz
    except ImportError:
        _write_image_pdf_with_pillow(path, text)
        return

    document = fitz.open()
    page = document.new_page(width=612, height=792)
    page.insert_textbox(
        fitz.Rect(72, 72, 540, 720),
        textwrap.dedent(text).strip(),
        fontsize=12,
        fontname="helv",
        align=0,
    )
    document.save(path)
    document.close()


def _write_image_pdf_with_pillow(path: Path, text: str = SAMPLE_TEXT) -> None:
    from PIL import Image, ImageDraw

    image = Image.new("RGB", (1240, 1754), "white")
    draw = ImageDraw.Draw(image)
    y = 120
    for line in textwrap.wrap(" ".join(text.split()), width=74):
        draw.text((120, y), line, fill="black")
        y += 34
    image.save(path, "PDF", resolution=150.0)


def extract_text_from_pdf(pdf_path: str | Path, force_ocr: bool = False, dpi: int = 200) -> str:
    """
    Extract text from a PDF. Native embedded text is used first; OCR is used for
    image-only pages or when force_ocr=True.
    """
    try:
        import fitz
    except ImportError as exc:
        raise RuntimeError(
            "PyMuPDF is required for PDF reading. Install dependencies with "
            "`python -m pip install -r requirements.txt`."
        ) from exc

    path = Path(pdf_path)
    document = fitz.open(path)
    pages: list[str] = []
    for page_index, page in enumerate(document, start=1):
        text = "" if force_ocr else page.get_text("text").strip()
        if not text:
            text = _ocr_page(page, dpi=dpi)
        pages.append(f"--- Page {page_index} ---\n{text.strip()}")
    document.close()
    return "\n\n".join(page for page in pages if page.strip())


def _ocr_page(page: Any, dpi: int = 200) -> str:
    try:
        import fitz
        import pytesseract
        from PIL import Image
    except ImportError as exc:
        raise RuntimeError(
            "OCR requires PyMuPDF, Pillow, and pytesseract. Install Python "
            "dependencies and the Tesseract OCR application."
        ) from exc

    zoom = dpi / 72
    pixmap = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
    image = Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)
    try:
        return pytesseract.image_to_string(image)
    except pytesseract.TesseractNotFoundError as exc:
        raise RuntimeError(
            "pytesseract is installed, but the Tesseract OCR application is not "
            "on PATH. Install Tesseract, then rerun the notebook."
        ) from exc


def chunk_text(text: str, max_chars: int = 1200, overlap: int = 150) -> list[str]:
    """Split text into small overlapping chunks that fit comfortably in prompts."""
    if max_chars <= 0:
        raise ValueError("max_chars must be positive")
    if overlap < 0 or overlap >= max_chars:
        raise ValueError("overlap must be non-negative and smaller than max_chars")

    clean_text = " ".join(text.split())
    if not clean_text:
        return []

    chunks: list[str] = []
    start = 0
    while start < len(clean_text):
        end = min(start + max_chars, len(clean_text))
        if end < len(clean_text):
            split_at = clean_text.rfind(" ", start, end)
            if split_at > start:
                end = split_at
        chunk = clean_text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= len(clean_text):
            break
        start = max(end - overlap, start + 1)
    return chunks


def prepare_demo_corpus(corpus_dir: str | Path = "data/corpus") -> list[Path]:
    """Create a tiny multi-document PDF corpus for the expanded tutorial."""
    directory = Path(corpus_dir)
    directory.mkdir(parents=True, exist_ok=True)
    pdf_paths: list[Path] = []
    for filename, text in DEMO_CORPUS_TEXTS:
        path = directory / filename
        if not path.exists():
            _write_text_pdf(path, text)
        pdf_paths.append(path)
    return pdf_paths


def load_corpus_documents(paths: Iterable[str | Path]) -> list[CorpusDocument]:
    """Load multiple PDFs into document records, skipping files that fail to parse."""
    documents: list[CorpusDocument] = []
    for pdf_path in paths:
        path = Path(pdf_path)
        try:
            text = extract_text_from_pdf(path)
        except Exception:
            text = _demo_corpus_text_for_path(path)
            if text is None:
                continue
        if not text.strip():
            continue
        document_id = _stable_doc_id(path.name, [text])
        documents.append(
            CorpusDocument(
                document_id=document_id,
                source_name=path.name,
                path=str(path),
                text=text,
            )
        )
    return documents


def _demo_corpus_text_for_path(path: Path) -> str | None:
    for filename, text in DEMO_CORPUS_TEXTS:
        if path.name == filename:
            return textwrap.dedent(text).strip()
    return None


def chunk_corpus_documents(
    documents: Iterable[CorpusDocument | dict[str, Any]],
    max_chars: int = 1200,
    overlap: int = 150,
) -> list[ChunkRecord]:
    """Chunk a corpus while preserving document metadata on every chunk."""
    records: list[ChunkRecord] = []
    for document in documents:
        data = _as_dict(document)
        text_chunks = chunk_text(data.get("text", ""), max_chars=max_chars, overlap=overlap)
        for index, chunk in enumerate(text_chunks):
            document_id = data["document_id"]
            records.append(
                ChunkRecord(
                    chunk_id=f"{document_id}:{index}",
                    document_id=document_id,
                    source_name=data["source_name"],
                    chunk_index=index,
                    text=chunk,
                )
            )
    return records


def load_demo_ontology(path: str | Path = "ontology/demo_ontology.yml") -> dict[str, Any]:
    """Load the lightweight YAML ontology used by the notebook demo."""
    import yaml

    ontology_path = Path(path)
    with ontology_path.open("r", encoding="utf-8") as handle:
        ontology = yaml.safe_load(handle) or {}
    ontology.setdefault("entity_types", [])
    ontology.setdefault("canonical_entities", {})
    ontology.setdefault("relationship_types", [])
    return ontology


def normalize_entities_with_ontology(
    entities: Iterable[Entity | dict[str, Any]],
    ontology: dict[str, Any],
) -> list[Entity]:
    """Replace ontology aliases with canonical entity names."""
    alias_index = _ontology_alias_index(ontology)
    normalized: list[Entity] = []
    for entity in entities:
        data = _as_dict(entity)
        raw_name = _clean_name(data.get("name", ""))
        canonical_name = alias_index.get(raw_name.casefold(), raw_name)
        ontology_entity = ontology.get("canonical_entities", {}).get(canonical_name, {})
        normalized.append(
            Entity(
                name=canonical_name,
                type=ontology_entity.get("type", data.get("type", "Unknown")),
                description=ontology_entity.get("description", data.get("description", "")),
                evidence=data.get("evidence", ""),
            )
        )
    return normalized


def resolve_entities(
    entities: Iterable[Entity | dict[str, Any]],
    ontology: dict[str, Any],
) -> tuple[list[ResolvedEntity], dict[str, str]]:
    """Merge duplicate entities using ontology aliases and simple name cleanup."""
    alias_index = _ontology_alias_index(ontology)
    canonical_entities = ontology.get("canonical_entities", {})
    grouped: dict[str, ResolvedEntity] = {}
    resolution_map: dict[str, str] = {}

    for entity in entities:
        data = _as_dict(entity)
        raw_name = _clean_name(data.get("name", ""))
        if not raw_name:
            continue
        canonical_name = alias_index.get(raw_name.casefold(), raw_name)
        ontology_entity = canonical_entities.get(canonical_name, {})
        resolved = grouped.setdefault(
            canonical_name,
            ResolvedEntity(
                canonical_name=canonical_name,
                type=ontology_entity.get("type", data.get("type", "Unknown")),
                description=ontology_entity.get("description", data.get("description", "")),
            ),
        )
        _append_unique(resolved.aliases, raw_name)
        _append_unique(resolved.aliases, canonical_name)
        _append_unique(resolved.source_names, data.get("source_name"))
        _append_unique(resolved.evidence, data.get("evidence"))
        resolution_map[raw_name] = canonical_name
        resolution_map[canonical_name] = canonical_name

    for canonical_name, ontology_entity in canonical_entities.items():
        for alias in ontology_entity.get("aliases", []):
            resolution_map.setdefault(alias, canonical_name)

    return list(grouped.values()), resolution_map


def resolve_relationships(
    relationships: Iterable[Relationship | dict[str, Any]],
    entity_resolution_map: dict[str, str],
) -> list[ResolvedRelationship]:
    """Resolve relationship endpoints to canonical entity names and deduplicate."""
    lower_resolution_map = {
        key.casefold(): value for key, value in entity_resolution_map.items()
    }
    grouped: dict[tuple[str, str, str], ResolvedRelationship] = {}

    for relationship in relationships:
        data = _as_dict(relationship)
        source = _resolve_name(data.get("source", ""), entity_resolution_map, lower_resolution_map)
        target = _resolve_name(data.get("target", ""), entity_resolution_map, lower_resolution_map)
        if not source or not target:
            continue
        rel_type = _safe_relationship_type(data.get("relationship", "RELATED_TO"))
        key = (source, target, rel_type)
        resolved = grouped.setdefault(
            key,
            ResolvedRelationship(
                source=source,
                target=target,
                relationship=rel_type,
                description=data.get("description", ""),
            ),
        )
        _append_unique(resolved.source_names, data.get("source_name"))
        _append_unique(resolved.evidence, data.get("evidence"))

    return list(grouped.values())


def semantic_search_chunks(
    client: Any,
    query: str,
    collection_name: str | None = None,
    limit: int = 5,
) -> list[dict[str, Any]]:
    """Search stored chunks, preferring vector search and falling back to BM25."""
    collection = client.collections.get(collection_name or os.getenv("WEAVIATE_COLLECTION", "OcrChunk"))
    try:
        response = collection.query.near_text(query=query, limit=limit)
    except Exception:
        response = _bm25_or_fetch_chunks(collection, query, limit)
    return [_weaviate_object_to_dict(obj) for obj in getattr(response, "objects", [])]


def classify_template_question(question: str) -> str:
    """Map a natural-language question to one of the stable tutorial templates."""
    normalized = question.casefold()
    if "drought" in normalized and any(term in normalized for term in ["dataset", "data", "imagery", "sensor"]):
        return "datasets_for_drought_planning"
    if any(term in normalized for term in ["organization", "organizations", "who"]) and "share" in normalized:
        return "organizations_sharing_data"
    if "method" in normalized and any(term in normalized for term in ["satellite", "imagery", "remote sensing"]):
        return "methods_for_satellite_imagery"
    return "general"


def template_hybrid_query(
    question: str,
    neo4j_driver: Any,
    weaviate_client: Any,
    limit: int = 5,
) -> dict[str, Any]:
    """Run a stable graph query plus chunk retrieval for a natural-language question."""
    intent = classify_template_question(question)
    cypher = _template_cypher(intent)
    with neo4j_driver.session() as session:
        graph_rows = session.run(cypher, limit=limit).data()
    chunks = semantic_search_chunks(weaviate_client, question, limit=limit)
    return {
        "question": question,
        "intent": intent,
        "graph_rows": graph_rows,
        "chunks": chunks,
    }


def llm_hybrid_query(
    question: str,
    graph_rows: list[dict[str, Any]],
    chunks: list[dict[str, Any]],
    client: Any | None = None,
    model: str | None = None,
) -> str:
    """Optional LLM answer synthesis from already-retrieved graph and chunk context."""
    client = client or _openai_client()
    context = {
        "question": question,
        "graph_rows": graph_rows,
        "chunks": chunks,
    }
    response = client.chat.completions.create(
        model=model or os.getenv("OPENAI_MODEL", "qwen3"),
        messages=[
            {
                "role": "system",
                "content": (
                    "Answer using only the provided graph rows and retrieved text chunks. "
                    "If the context is insufficient, say what is missing."
                ),
            },
            {
                "role": "user",
                "content": json.dumps(context, indent=2),
            },
        ],
    )
    return response.choices[0].message.content or ""


def _template_cypher(intent: str) -> str:
    if intent == "datasets_for_drought_planning":
        return """
        MATCH (dataset:Entity)
        WHERE dataset.type = 'Dataset'
        OPTIONAL MATCH (dataset)-[r]-(topic:Entity)
        WHERE topic.name = 'Drought Planning'
        RETURN dataset.name AS dataset,
               collect(DISTINCT type(r)) AS relationships,
               collect(DISTINCT topic.name) AS connected_to
        ORDER BY dataset
        LIMIT $limit
        """
    if intent == "organizations_sharing_data":
        return """
        MATCH (organization:Entity)-[r:SHARES_WITH]-(other:Entity)
        WHERE organization.type = 'Organization'
        RETURN organization.name AS organization,
               other.name AS shares_with,
               r.description AS description
        ORDER BY organization
        LIMIT $limit
        """
    if intent == "methods_for_satellite_imagery":
        return """
        MATCH (method:Entity)-[r]-(dataset:Entity)
        WHERE method.type = 'Method'
          AND dataset.name = 'Satellite Imagery'
        RETURN method.name AS method,
               type(r) AS relationship,
               dataset.name AS dataset
        ORDER BY method
        LIMIT $limit
        """
    return """
    MATCH (entity:Entity)
    RETURN entity.name AS entity,
           entity.type AS type,
           entity.description AS description
    ORDER BY entity.name
    LIMIT $limit
    """


def _bm25_or_fetch_chunks(collection: Any, query: str, limit: int) -> Any:
    try:
        return collection.query.bm25(query=query, query_properties=["text"], limit=limit)
    except TypeError:
        return collection.query.bm25(query=query, limit=limit)
    except Exception:
        return collection.query.fetch_objects(limit=limit)


def _weaviate_object_to_dict(obj: Any) -> dict[str, Any]:
    properties = dict(getattr(obj, "properties", {}) or {})
    result = {
        "text": properties.get("text", ""),
        "source_name": properties.get("source_name", ""),
        "chunk_index": properties.get("chunk_index"),
    }
    metadata = getattr(obj, "metadata", None)
    if metadata is not None and getattr(metadata, "distance", None) is not None:
        result["distance"] = metadata.distance
    return result


def connect_weaviate():
    """Connect to the local Weaviate service from docker-compose.yml."""
    import warnings
    from json import JSONDecodeError as StdlibJSONDecodeError

    from requests import exceptions as requests_exceptions

    # Expanse provides requests 2.25.1, while Weaviate imports the
    # requests.exceptions.JSONDecodeError name added in requests 2.27.
    if not hasattr(requests_exceptions, "JSONDecodeError"):
        requests_exceptions.JSONDecodeError = StdlibJSONDecodeError

    warnings.filterwarnings(
        "ignore",
        message="Python 3.8 is no longer supported by the Python core team.*",
    )

    import weaviate

    return weaviate.connect_to_local(
        host=os.getenv("WEAVIATE_HTTP_HOST", "localhost"),
        port=int(os.getenv("WEAVIATE_HTTP_PORT", "18080")),
        grpc_port=int(os.getenv("WEAVIATE_GRPC_PORT", "15051")),
    )


def load_chunks_into_weaviate(
    client: Any,
    chunks: Iterable[str | ChunkRecord | dict[str, Any]],
    source_name: str | None = None,
    collection_name: str | None = None,
) -> dict[str, Any]:
    """Create a simple OCR chunk collection and load chunks into Weaviate."""
    chunk_list = list(chunks)
    collection_name = collection_name or os.getenv("WEAVIATE_COLLECTION", "OcrChunk")
    collection = _ensure_ocr_collection(client, collection_name)
    chunk_properties = _weaviate_chunk_properties(chunk_list, source_name)
    doc_ids = list(dict.fromkeys(properties["doc_id"] for properties in chunk_properties))
    doc_id = doc_ids[0] if len(doc_ids) == 1 else _stable_doc_id(source_name or "corpus", [p["text"] for p in chunk_properties])

    if chunk_properties:
        try:
            from weaviate.classes.query import Filter

            for current_doc_id in doc_ids:
                collection.data.delete_many(where=Filter.by_property("doc_id").equal(current_doc_id))
        except Exception:
            pass

    with collection.batch.dynamic() as batch:
        for index, properties in enumerate(chunk_properties):
            batch.add_object(
                uuid=str(uuid.uuid5(uuid.NAMESPACE_URL, f"{properties['doc_id']}:{properties['chunk_index']}:{index}")),
                properties=properties,
            )

    return {
        "collection": collection_name,
        "doc_id": doc_id,
        "chunks_loaded": len(chunk_properties),
    }


def _ensure_ocr_collection(client: Any, collection_name: str):
    if client.collections.exists(collection_name):
        return client.collections.get(collection_name)

    from weaviate.classes.config import DataType, Property

    return client.collections.create(
        name=collection_name,
        properties=[
            Property(name="doc_id", data_type=DataType.TEXT),
            Property(name="source_name", data_type=DataType.TEXT),
            Property(name="chunk_index", data_type=DataType.INT),
            Property(name="text", data_type=DataType.TEXT),
        ],
    )


def _weaviate_chunk_properties(
    chunks: list[str | ChunkRecord | dict[str, Any]],
    source_name: str | None,
) -> list[dict[str, Any]]:
    if not chunks:
        return []

    if all(isinstance(chunk, str) for chunk in chunks):
        if not source_name:
            raise ValueError("source_name is required when loading plain text chunks")
        text_chunks = [str(chunk) for chunk in chunks]
        doc_id = _stable_doc_id(source_name, text_chunks)
        return [
            {
                "doc_id": doc_id,
                "source_name": source_name,
                "chunk_index": index,
                "text": chunk,
            }
            for index, chunk in enumerate(text_chunks)
        ]

    properties: list[dict[str, Any]] = []
    for index, chunk in enumerate(chunks):
        data = _as_dict(chunk)
        document_id = data.get("document_id") or data.get("doc_id")
        if not document_id:
            if not source_name:
                raise ValueError("chunk records must include document_id or source_name must be provided")
            document_id = _stable_doc_id(source_name, [data.get("text", "")])
        properties.append(
            {
                "doc_id": document_id,
                "source_name": data.get("source_name", source_name or ""),
                "chunk_index": int(data.get("chunk_index", index)),
                "text": data.get("text", ""),
            }
        )
    return properties


def _stable_doc_id(source_name: str, chunks: list[str]) -> str:
    digest = hashlib.sha256()
    digest.update(source_name.encode("utf-8"))
    for chunk in chunks:
        digest.update(chunk.encode("utf-8"))
    return digest.hexdigest()[:16]


def extract_entities(text: str, client: Any | None = None, model: str | None = None) -> list[Entity]:
    """First LLM call: extract all document entities from the full OCR text."""
    client = client or _openai_client()
    response = client.beta.chat.completions.parse(
        model=model or os.getenv("OPENAI_MODEL", "qwen3"),
        messages=[
            {
                "role": "system",
                "content": (
                    "You extract every supported entity from OCR text. "
                    "Keep names canonical, avoid duplicates, and do not limit "
                    "the number of entities."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Extract all entities from this OCR text. "
                    "Return only entities that are directly supported by the text.\n\n"
                    f"{text}"
                ),
            },
        ],
        response_format=EntityExtraction,
    )
    return response.choices[0].message.parsed.entities


def extract_relationships(
    text: str,
    entities: Iterable[Entity | dict[str, Any]],
    client: Any | None = None,
    model: str | None = None,
) -> list[Relationship]:
    """Extract all relationships using the entity list and full OCR text."""
    client = client or _openai_client()
    entity_payload = [_as_dict(entity) for entity in entities]
    response = client.beta.chat.completions.parse(
        model=model or os.getenv("OPENAI_MODEL", "qwen3"),
        messages=[
            {
                "role": "system",
                "content": (
                    "You extract entity-to-entity relationships for a knowledge graph. "
                    "Use only the provided entity names as source and target values. "
                    "Do not limit the number of supported relationships."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Entity list:\n"
                    f"{json.dumps(entity_payload, indent=2)}\n\n"
                    "OCR text:\n"
                    f"{text}\n\n"
                    "Extract all relationships supported by the OCR text. The source "
                    "and target must exactly match names from the entity list."
                ),
            },
        ],
        response_format=RelationshipExtraction,
    )
    return response.choices[0].message.parsed.relationships


def _openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Set OPENAI_API_KEY to your NRP LLM token before running the LLM cells.")
    from openai import OpenAI

    return OpenAI(api_key=api_key, base_url="https://ellm.nrp-nautilus.io/v1")


def write_graph_to_neo4j(
    entities: Iterable[Entity | dict[str, Any]],
    relationships: Iterable[Relationship | dict[str, Any]],
    document_name: str,
    uri: str | None = None,
    username: str | None = None,
    password: str | None = None,
) -> dict[str, int]:
    """Write extracted entities and relationships to Neo4j with simple MERGE queries."""
    from neo4j import GraphDatabase

    uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
    username = username or os.getenv("NEO4J_USERNAME", "neo4j")
    password = password or os.getenv("NEO4J_PASSWORD", "please-change-me")
    entity_list = [_as_dict(entity) for entity in entities]
    relationship_list = [_as_dict(relationship) for relationship in relationships]

    driver = GraphDatabase.driver(uri, auth=(username, password))
    with driver:
        with driver.session() as session:
            session.run(
                "MERGE (d:Document {name: $document_name})",
                document_name=document_name,
            )
            for entity in entity_list:
                session.run(
                    """
                    MATCH (d:Document {name: $document_name})
                    MERGE (e:Entity {name: $name})
                    SET e.type = $type,
                        e.description = $description,
                        e.evidence = $evidence
                    MERGE (d)-[:MENTIONS]->(e)
                    """,
                    document_name=document_name,
                    name=entity["name"],
                    type=entity.get("type", "Unknown"),
                    description=entity.get("description", ""),
                    evidence=entity.get("evidence", ""),
                )
            for relationship in relationship_list:
                rel_type = _safe_relationship_type(relationship.get("relationship", "RELATED_TO"))
                session.run(
                    f"""
                    MATCH (source:Entity {{name: $source}})
                    MATCH (target:Entity {{name: $target}})
                    MERGE (source)-[r:{rel_type}]->(target)
                    SET r.description = $description,
                        r.evidence = $evidence
                    """,
                    source=relationship["source"],
                    target=relationship["target"],
                    description=relationship.get("description", ""),
                    evidence=relationship.get("evidence", ""),
                )

    return {
        "documents_written": 1,
        "entities_written": len(entity_list),
        "relationships_written": len(relationship_list),
    }


def write_resolved_graph_to_neo4j(
    entities: Iterable[ResolvedEntity | dict[str, Any]],
    relationships: Iterable[ResolvedRelationship | dict[str, Any]],
    documents: Iterable[CorpusDocument | dict[str, Any]] | None = None,
    driver: Any | None = None,
    uri: str | None = None,
    username: str | None = None,
    password: str | None = None,
) -> dict[str, int]:
    """Write normalized corpus entities and relationships to Neo4j."""
    entity_list = [_as_dict(entity) for entity in entities]
    relationship_list = [_as_dict(relationship) for relationship in relationships]
    document_list = [_as_dict(document) for document in documents or []]
    close_driver = False

    if driver is None:
        from neo4j import GraphDatabase

        uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
        username = username or os.getenv("NEO4J_USERNAME", "neo4j")
        password = password or os.getenv("NEO4J_PASSWORD", "please-change-me")
        driver = GraphDatabase.driver(uri, auth=(username, password))
        close_driver = True

    try:
        with driver.session() as session:
            for document in document_list:
                session.run(
                    """
                    MERGE (d:Document {document_id: $document_id})
                    SET d.source_name = $source_name,
                        d.path = $path
                    """,
                    document_id=document["document_id"],
                    source_name=document["source_name"],
                    path=document.get("path", ""),
                )

            for entity in entity_list:
                session.run(
                    """
                    MERGE (e:Entity {name: $name})
                    SET e.type = $type,
                        e.description = $description,
                        e.aliases = $aliases,
                        e.evidence = $evidence
                    """,
                    name=entity["canonical_name"],
                    type=entity.get("type", "Unknown"),
                    description=entity.get("description", ""),
                    aliases=entity.get("aliases", []),
                    evidence=entity.get("evidence", []),
                )
                for source_name in entity.get("source_names", []):
                    session.run(
                        """
                        MERGE (d:Document {source_name: $source_name})
                        WITH d
                        MATCH (e:Entity {name: $name})
                        MERGE (d)-[:MENTIONS]->(e)
                        """,
                        source_name=source_name,
                        name=entity["canonical_name"],
                    )

            for relationship in relationship_list:
                rel_type = _safe_relationship_type(relationship.get("relationship", "RELATED_TO"))
                session.run(
                    f"""
                    MATCH (source:Entity {{name: $source}})
                    MATCH (target:Entity {{name: $target}})
                    MERGE (source)-[r:{rel_type}]->(target)
                    SET r.description = $description,
                        r.evidence = $evidence,
                        r.source_names = $source_names
                    """,
                    source=relationship["source"],
                    target=relationship["target"],
                    description=relationship.get("description", ""),
                    evidence=relationship.get("evidence", []),
                    source_names=relationship.get("source_names", []),
                )
    finally:
        if close_driver:
            driver.close()

    return {
        "documents_written": len(document_list),
        "entities_written": len(entity_list),
        "relationships_written": len(relationship_list),
    }


def _safe_relationship_type(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_]+", "_", value.upper()).strip("_")
    if not cleaned:
        return "RELATED_TO"
    if cleaned[0].isdigit():
        cleaned = f"REL_{cleaned}"
    return cleaned


def _ontology_alias_index(ontology: dict[str, Any]) -> dict[str, str]:
    index: dict[str, str] = {}
    for canonical_name, details in ontology.get("canonical_entities", {}).items():
        index[_clean_name(canonical_name).casefold()] = canonical_name
        for alias in details.get("aliases", []):
            index[_clean_name(alias).casefold()] = canonical_name
    return index


def _clean_name(value: Any) -> str:
    return " ".join(str(value or "").split())


def _append_unique(values: list[str], value: Any) -> None:
    if not value:
        return
    item = str(value)
    if item not in values:
        values.append(item)


def _resolve_name(
    value: Any,
    resolution_map: dict[str, str],
    lower_resolution_map: dict[str, str],
) -> str:
    raw_name = _clean_name(value)
    return resolution_map.get(raw_name) or lower_resolution_map.get(raw_name.casefold(), raw_name)


def _as_dict(value: Any) -> dict[str, Any]:
    if hasattr(value, "model_dump"):
        return value.model_dump()
    if isinstance(value, dict):
        return value
    return dict(value)
