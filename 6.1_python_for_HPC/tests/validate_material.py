#!/usr/bin/env python3
"""Static validation for the Python for HPC lesson."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


SESSION_ROOT = Path(__file__).resolve().parents[1]
GENERATED_DIRECTORIES = {"test-results", ".ipynb_checkpoints"}


def is_source_file(path: Path) -> bool:
    relative = path.relative_to(SESSION_ROOT)
    return not GENERATED_DIRECTORIES.intersection(relative.parts)


NOTEBOOKS = sorted(
    path for path in SESSION_ROOT.glob("**/*.ipynb") if is_source_file(path)
)
SHELL_FILES = sorted(
    {
        *(
            path
            for path in SESSION_ROOT.glob("**/*.sh")
            if is_source_file(path)
        ),
        *(
            path
            for path in SESSION_ROOT.glob("**/*.slurm")
            if is_source_file(path)
        ),
        *(
            path
            for path in SESSION_ROOT.glob("**/*.slrm")
            if is_source_file(path)
        ),
    }
)
TEXT_SUFFIXES = {".md", ".py", ".sh", ".slurm", ".slrm", ".yaml", ".yml"}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate_notebooks(errors: list[str]) -> None:
    for path in NOTEBOOKS:
        relative = path.relative_to(SESSION_ROOT)
        try:
            notebook = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            fail(errors, f"{relative}: invalid JSON: {exc}")
            continue

        if notebook.get("nbformat") != 4:
            fail(errors, f"{relative}: expected notebook format 4")
        cells = notebook.get("cells", [])
        if not cells:
            fail(errors, f"{relative}: notebook has no cells")
            continue

        markdown_text = "\n".join(
            "".join(cell.get("source", []))
            for cell in cells
            if cell.get("cell_type") == "markdown"
        )
        introduction = "".join(cells[0].get("source", []))
        if not re.search(
            r"\*\*(?:Core notebook|Core capstone|Optional deep dive),",
            introduction,
        ):
            fail(errors, f"{relative}: first cell does not label its lesson tier")
        if "## Takeaway" not in markdown_text:
            fail(errors, f"{relative}: missing a Takeaway section")

        cell_ids = [cell.get("id") for cell in cells if cell.get("id")]
        if len(cell_ids) != len(set(cell_ids)):
            fail(errors, f"{relative}: contains duplicate cell IDs")

        for index, cell in enumerate(cells):
            if cell.get("cell_type") not in {"markdown", "code", "raw"}:
                fail(errors, f"{relative}: cell {index} has invalid type")
            if "source" not in cell:
                fail(errors, f"{relative}: cell {index} has no source")
            if cell.get("cell_type") == "code" and cell.get("outputs"):
                fail(errors, f"{relative}: cell {index} contains saved output")
            if (
                cell.get("cell_type") == "code"
                and cell.get("execution_count") is not None
            ):
                fail(
                    errors,
                    f"{relative}: cell {index} has a saved execution count",
                )


def validate_lesson_alignment(errors: list[str]) -> None:
    required_snippets = {
        "3_numba/0_basics.ipynb": ("**12 minutes.**",),
        "4_threads_vs_processes/threads_vs_processes.ipynb": (
            "**12 minutes.**",
            "n_workers = min(4, os.cpu_count() or 1)",
        ),
        "5_dask/1_delayed.ipynb": ("**5 minutes.**",),
        "5_dask/2_multicore_array.ipynb": (
            "**10 minutes.**",
            "da.sin(dask_array) * dask_array * da.log(dask_array)",
        ),
        "5_dask/4_multinode_distributed_array.ipynb": (
            "18 minutes hands-on",
            "client.wait_for_workers(2",
            "assert len(worker_hosts) >= 2",
            "da.sin(array) * array * da.log(array)",
        ),
        "2_ai_code_assist/README.md": ("**8 minutes.**",),
        "README.md": (
            "reserve 57 minutes",
            "or about 34% of the full session",
            "Slides 39 to 43",
            "optional appendix",
        ),
        "slides/SLIDES.md": (
            "12 minutes. Blue means help. Yellow means ready.",
            "12 minutes. Discuss with a neighbor.",
            "18 minutes. Clean up before moving on.",
            "Give eight minutes.",
            "4 of 7 | Break",
            "5 of 7 | Dask tasks and chunks",
            "7 of 7 | Recap",
            "It creates or reuses the pythonhpc Conda environment.",
            "The GIL is a CPython rule",
            "A task graph is a plan",
            "Save the job number. Wait for two workers.",
            'Stop before "Build an array across the workers."',
            "OPTIONAL | AI-assisted workflow",
        ),
    }

    for relative, snippets in required_snippets.items():
        text = (SESSION_ROOT / relative).read_text(encoding="utf-8")
        for snippet in snippets:
            if snippet not in text:
                fail(
                    errors,
                    f"{relative}: missing aligned lesson text: {snippet}",
                )

    slide_text = (SESSION_ROOT / "slides/SLIDES.md").read_text(
        encoding="utf-8"
    )
    slide_count = len(re.split(r"^---$", slide_text, flags=re.MULTILINE))
    if slide_count != 43:
        fail(
            errors,
            f"slides/SLIDES.md: expected 43 slides, found {slide_count}",
        )


def validate_shell(errors: list[str]) -> None:
    for path in SHELL_FILES:
        result = subprocess.run(
            ["bash", "-n", str(path)],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode:
            fail(
                errors,
                f"{path.relative_to(SESSION_ROOT)}: bash -n failed: "
                f"{result.stderr.strip()}",
            )


def validate_production_slurm(errors: list[str]) -> None:
    required = {
        "0_python_condaenv_scratch/python_expanse.slurm",
        "dask_slurm/dask_workers.slrm",
    }
    directives = {
        "#SBATCH --account=sdp173",
        "#SBATCH --partition=compute",
        "#SBATCH --reservation=si26cpu",
        "#SBATCH --qos=normal-eot",
    }
    for relative in required:
        text = (SESSION_ROOT / relative).read_text(encoding="utf-8")
        for directive in directives:
            if directive not in text:
                fail(errors, f"{relative}: missing {directive}")

    worker_script = (
        SESSION_ROOT / "dask_slurm/dask_workers.slrm"
    ).read_text(encoding="utf-8")
    if "#SBATCH --time=00:30:00" not in worker_script:
        fail(
            errors,
            "dask_slurm/dask_workers.slrm: expected a 30-minute limit",
        )

    compute_launcher = (
        SESSION_ROOT / "launch_galyleo_compute.sh"
    ).read_text(encoding="utf-8")
    for flag in (
        "--account sdp173",
        "--partition compute",
        "--reservation si26cpu",
        "--qos normal-eot",
    ):
        if flag not in compute_launcher:
            fail(errors, f"launch_galyleo_compute.sh: missing {flag}")

    shared_launcher = (
        SESSION_ROOT / "1_python_singularity/launch_galyleo_singularity.sh"
    ).read_text(encoding="utf-8")
    for flag in (
        "--account sdp173",
        "--partition shared",
        "--reservation si26cpu",
    ):
        if flag not in shared_launcher:
            fail(
                errors,
                "1_python_singularity/launch_galyleo_singularity.sh: "
                f"missing {flag}",
            )
    if re.search(r"^\s*--qos\b", shared_launcher, flags=re.MULTILINE):
        fail(
            errors,
            "shared Galyleo launcher sets a QOS, but main documents no shared QOS",
        )


def validate_environments(errors: list[str]) -> None:
    environment = (SESSION_ROOT / "environment.yaml").read_text(encoding="utf-8")
    required_packages = {
        "python=3.12",
        "dask",
        "distributed",
        "graphviz",
        "numba",
        "psutil",
    }
    for package in required_packages:
        if f"- {package}" not in environment:
            fail(errors, f"environment.yaml: missing {package}")

    definition = (
        SESSION_ROOT
        / "1_python_singularity/singularity_container/"
        "Singularity.anaconda3-dask-numba"
    ).read_text(encoding="utf-8")
    for text in ("'python==3.12'", "%test", "import numpy, numba, dask"):
        if text not in definition:
            fail(errors, f"Singularity definition: missing {text}")


def validate_text(errors: list[str]) -> None:
    stale_patterns = {
        "gue998": re.compile(r"\bgue998\b"),
        "SI25": re.compile(r"\bSI25\b"),
        "si25cpu": re.compile(r"\bsi25cpu\b"),
        "wrong dashboard port": re.compile(r"proxy/22222"),
    }
    unclear_student_phrases = {
        "steady-state": re.compile(r"\bsteady-state\b", re.IGNORECASE),
        "nopython": re.compile(r"\bnopython\b", re.IGNORECASE),
        "njit": re.compile(r"\bnjit\b"),
        "directed acyclic graph": re.compile(
            r"\bdirected acyclic graph\b", re.IGNORECASE
        ),
        "serialization": re.compile(r"\bserialization\b", re.IGNORECASE),
        "CPU-bound": re.compile(r"\bCPU-bound\b", re.IGNORECASE),
        "hot loop": re.compile(r"\bhot loop\b", re.IGNORECASE),
        "oversubscription": re.compile(
            r"\boversubscription\b", re.IGNORECASE
        ),
    }

    for path in sorted(SESSION_ROOT.glob("**/*")):
        if not path.is_file():
            continue
        if not is_source_file(path):
            continue
        if path.resolve() == Path(__file__).resolve():
            continue
        if path.suffix not in TEXT_SUFFIXES and path.suffix != ".ipynb":
            continue
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(SESSION_ROOT)
        if "\u2014" in text:
            fail(errors, f"{relative}: contains an em dash")
        for label, pattern in stale_patterns.items():
            if pattern.search(text):
                fail(errors, f"{relative}: contains stale value: {label}")
        for label, pattern in unclear_student_phrases.items():
            if pattern.search(text):
                fail(
                    errors,
                    f"{relative}: contains unclear student phrase: {label}",
                )


def validate_markdown_links(errors: list[str]) -> None:
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for path in sorted(
        path
        for path in SESSION_ROOT.glob("**/*.md")
        if is_source_file(path)
    ):
        text = path.read_text(encoding="utf-8")
        for target in link_pattern.findall(text):
            clean_target = target.split("#", 1)[0]
            if (
                not clean_target
                or "://" in clean_target
                or clean_target.startswith("mailto:")
            ):
                continue
            resolved = (path.parent / clean_target).resolve()
            if not resolved.exists():
                fail(
                    errors,
                    f"{path.relative_to(SESSION_ROOT)}: broken link {target}",
                )


def main() -> int:
    errors: list[str] = []
    validate_notebooks(errors)
    validate_lesson_alignment(errors)
    validate_shell(errors)
    validate_production_slurm(errors)
    validate_environments(errors)
    validate_text(errors)
    validate_markdown_links(errors)

    if errors:
        print("Material validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"Material validation passed: {len(NOTEBOOKS)} notebooks, "
        f"{len(SHELL_FILES)} shell or SLURM files."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
