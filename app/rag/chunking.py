"""
Simple, dependency-free text chunker.

Splits on paragraph/sentence boundaries where possible, targeting
`chunk_size` words per chunk with `overlap` words repeated between
consecutive chunks (so context isn't lost at chunk edges).

Word-count is used as a cheap proxy for tokens — good enough for FAQ
and policy-style content. If you later ingest very long-form documents,
swap this for a proper tokenizer-aware splitter.
"""

from app.config import get_settings

settings = get_settings()


def chunk_text(
    text: str,
    chunk_size_words: int | None = None,
    overlap_words: int | None = None,
) -> list[str]:
    chunk_size_words = chunk_size_words or settings.chunk_size_tokens
    overlap_words = overlap_words or settings.chunk_overlap_tokens

    words = text.split()
    if not words:
        return []

    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size_words
        chunk = " ".join(words[start:end])
        if chunk.strip():
            chunks.append(chunk.strip())
        if end >= len(words):
            break
        start = end - overlap_words  # step back for overlap

    return chunks
