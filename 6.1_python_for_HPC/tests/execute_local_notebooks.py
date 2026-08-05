#!/usr/bin/env python3
"""Execute all lesson notebooks that do not require a distributed cluster."""

from __future__ import annotations

import json
import os
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import nbformat
from nbclient import NotebookClient


SESSION_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = SESSION_ROOT / "test-results"
SKIP = {Path("3_dask/4_multinode_distributed_array.ipynb")}
GENERATED_DIRECTORIES = {"test-results", ".ipynb_checkpoints"}
NOTEBOOKS = [
    path
    for path in sorted(SESSION_ROOT.glob("**/*.ipynb"))
    if (
        path.relative_to(SESSION_ROOT) not in SKIP
        and not GENERATED_DIRECTORIES.intersection(
            path.relative_to(SESSION_ROOT).parts
        )
    )
]


def execute(path: Path) -> dict[str, object]:
    started = time.perf_counter()
    relative = path.relative_to(SESSION_ROOT)
    notebook = nbformat.read(path, as_version=4)
    client = NotebookClient(
        notebook,
        timeout=300,
        kernel_name="python3",
        resources={"metadata": {"path": str(path.parent)}},
    )
    try:
        client.execute(cwd=str(path.parent))
    except Exception as exc:
        return {
            "notebook": str(relative),
            "status": "failed",
            "seconds": round(time.perf_counter() - started, 3),
            "error": f"{type(exc).__name__}: {exc}",
        }
    return {
        "notebook": str(relative),
        "status": "passed",
        "seconds": round(time.perf_counter() - started, 3),
    }


def main() -> int:
    os.environ["PYHPC_TEST_MODE"] = "1"
    os.environ.setdefault("NUMBA_NUM_THREADS", "4")
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
    os.environ.setdefault("MKL_NUM_THREADS", "1")

    RESULTS_DIR.mkdir(exist_ok=True)
    results = []
    for path in NOTEBOOKS:
        print(f"Executing {path.relative_to(SESSION_ROOT)}", flush=True)
        result = execute(path)
        results.append(result)
        print(
            f"  {result['status']} in {result['seconds']} seconds",
            flush=True,
        )

    summary = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "hostname": platform.node(),
        "python": sys.version,
        "test_mode": True,
        "results": results,
    }
    output = RESULTS_DIR / "local-notebooks.json"
    output.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    failures = [item for item in results if item["status"] != "passed"]
    print(f"Wrote {output}")
    if failures:
        for failure in failures:
            print(f"FAILED: {failure['notebook']}: {failure['error']}")
        return 1
    print(f"All {len(results)} local notebooks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
