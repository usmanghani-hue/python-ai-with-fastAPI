"""
Embedding generation — uses a free, local HuggingFace model
(sentence-transformers) instead of a paid API. Runs on your own
machine, no API key or billing needed.
"""

from sentence_transformers import SentenceTransformer

_model = SentenceTransformer("all-MiniLM-L6-v2")


async def embed_text(text: str) -> list[float]:
    embedding = _model.encode(text, convert_to_numpy=True)
    return embedding.tolist()


async def embed_batch(texts: list[str]) -> list[list[float]]:
    """Batch call — much faster than embedding one at a time during ingestion."""
    if not texts:
        return []
    embeddings = _model.encode(texts, convert_to_numpy=True)
    return [e.tolist() for e in embeddings]