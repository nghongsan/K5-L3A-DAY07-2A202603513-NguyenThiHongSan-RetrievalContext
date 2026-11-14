"""Rebuild the dense index from data/chunks.json when the Day 6 repo is not available.

Same model, prefix and metric as Day 6 (intfloat/multilingual-e5-small, "passage: ",
L2-normalised, Chroma HNSW cosine), same collection name and chunk IDs, so results are
comparable. Then run everything with CHROMA_PATH=<out>.

Usage:  python -m src.build_index --out index/chroma
"""
from __future__ import annotations

import argparse
import time

from .config import CHROMA_COLLECTION, EMBEDDING_DIM, EMBEDDING_MODEL
from .retrieval import load_chunks


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="index/chroma")
    a = ap.parse_args()
    import chromadb
    from sentence_transformers import SentenceTransformer

    chunks = load_chunks()
    t0 = time.perf_counter()
    model = SentenceTransformer(EMBEDDING_MODEL, device="cpu")
    vecs = model.encode(["passage: " + c["text"] for c in chunks], batch_size=32, normalize_embeddings=True,
                        show_progress_bar=False).tolist()
    if len(vecs[0]) != EMBEDDING_DIM:
        raise SystemExit("unexpected embedding dimension")
    client = chromadb.PersistentClient(path=a.out)
    col = client.get_or_create_collection(CHROMA_COLLECTION, embedding_function=None, metadata={
        "hnsw:space": "cosine", "embedding_model": EMBEDDING_MODEL, "dimensions": EMBEDDING_DIM})
    col.upsert(ids=[c["id"] for c in chunks], embeddings=vecs, documents=[c["text"] for c in chunks],
               metadatas=[{"document_id": c["source_id"], "page": c["page"], "chapter": c["metadata"]["chapter"],
                           "section": c["metadata"]["section"]} for c in chunks])
    print(f"indexed {col.count()} chunks into {a.out}/{CHROMA_COLLECTION} in {time.perf_counter() - t0:.1f}s")


if __name__ == "__main__":
    main()
