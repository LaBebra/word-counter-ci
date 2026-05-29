# word_counter.py
import re
from collections import Counter
from pathlib import Path


def read_file(filepath: str) -> str:
    """Read content from a .txt file and return it as a string."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    if path.suffix.lower() != ".txt":
        raise ValueError(f"File must have .txt extension, got: {path.suffix}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
    
def extract_words(text: str) -> list:
    """Extract all words from text, lowercased, ignoring punctuation."""
    words = re.findall(r"\b[a-zA-Zа-яА-ЯіІїЇєЄґҐ']+\b", text.lower())
    return words    