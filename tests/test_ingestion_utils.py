"""
Basic tests. Run with:
    pytest
"""

from app.rag.chunking import chunk_text
from app.utils.text_cleaning import basic_clean, clean_chat_history, is_low_value_turn


def test_chunk_text_splits_long_input():
    text = " ".join(["word"] * 1000)
    chunks = chunk_text(text, chunk_size_words=400, overlap_words=60)
    assert len(chunks) > 1
    # every chunk should have at most chunk_size_words words
    assert all(len(c.split()) <= 400 for c in chunks)


def test_chunk_text_empty_input_returns_empty_list():
    assert chunk_text("") == []


def test_basic_clean_collapses_whitespace():
    assert basic_clean("hello   world\n\n\n\nfoo") == "hello world\n\nfoo"


def is_low_value_turn(text: str) -> bool:
    """
    Detect short greetings or other low-value conversational turns
    that do not require RAG retrieval.
    """

    normalized = " ".join(text.lower().strip().split())

    greetings = {
        "hi",
        "hello",
        "hey",
        "salam",
        "aoa",
        "assalam o alaikum",
        "assalamualaikum",
        "good morning",
        "good afternoon",
        "good evening",
    }

    return normalized in greetings


def test_clean_chat_history_removes_filler_lines():
    raw = "Hi\nGermany ke liye requirements kya hain?\nThanks\n"
    cleaned = clean_chat_history(raw)
    assert "Germany" in cleaned
    assert "Hi" not in cleaned.split("\n")
