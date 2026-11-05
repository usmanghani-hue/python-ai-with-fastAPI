"""
Cleaning helpers applied before chunking — especially important for
raw human chat history, which is noisy (greetings, filler, duplicates).
"""

import re


def basic_clean(text: str) -> str:
    """Whitespace/formatting cleanup that applies to any source."""
    text = text.replace("\r\n", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


# Common low-value turns in support chat exports — extend this list as
# you observe more noise in your own chat history exports.
_FILLER_PATTERNS = [
    r"^\s*(hi|hello|hey|salam|assalam[o0]?\s*alaikum)[.!]?\s*$",
    r"^\s*(thank you|thanks|shukriya|jazakallah)[.!]?\s*$",
    r"^\s*(ok|okay|acha|theek hai|k)[.!]?\s*$",
]
_FILLER_RE = re.compile("|".join(_FILLER_PATTERNS), re.IGNORECASE)


def is_low_value_turn(line: str) -> bool:
    """True for greeting/filler-only lines that shouldn't become knowledge."""
    return bool(_FILLER_RE.match(line.strip()))


def clean_chat_history(raw_text: str) -> str:
    """
    Remove greeting/filler-only lines from a raw chat export, leaving
    the substantive Q&A content that ingestion should turn into chunks.
    """
    cleaned = basic_clean(raw_text)
    lines = [ln for ln in cleaned.split("\n") if ln.strip() and not is_low_value_turn(ln)]
    return "\n".join(lines)
