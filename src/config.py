"""Paths and settings shared by the Day 7 pipeline.

Day 6 artefacts (Chroma index + local e5 model) are reused as-is. Override the
location with DAY6_DIR. Secrets are read from the environment or from a local
``.env`` file (git-ignored); they are never printed or written to traces.
"""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RESULTS_DIR = ROOT / "results"

DAY6_DIR = Path(os.getenv(
    "DAY6_DIR", Path.home() / "Desktop" / "K5-L3-Day06-DataIngestionEngineering-main"))
CHROMA_PATH = Path(os.getenv("CHROMA_PATH", DAY6_DIR / "chroma_db"))   # or the rebuilt index from src.build_index
CHROMA_COLLECTION = "day06_C"          # Day 6 strategy C: paragraph chunks (<=800 chars) + metadata
EMBEDDING_MODEL = "intfloat/multilingual-e5-small"
EMBEDDING_DIM = 384

CHUNKS_FILE = DATA_DIR / "chunks.json"
BENCHMARK_FILE = DATA_DIR / "benchmark.json"


def load_dotenv(path: Path = ROOT / ".env") -> None:
    """Minimal .env loader (KEY=VALUE lines). Existing env vars win. Never logs values."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key, value = key.strip(), value.strip().strip('"').strip("'")
        if key and value and key not in os.environ:
            os.environ[key] = value
