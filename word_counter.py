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

def count_words(words: list) -> Counter:
    """Count occurrences of each word and return a Counter object."""
    return Counter(words)

def get_top_words(counter: Counter, n: int = 10) -> list:
    """Return the top n most common words as a list of (word, count) tuples."""
    if n <= 0:
        raise ValueError("n must be a positive integer")
    return counter.most_common(n)

def write_results(top_words: list, output_filepath: str) -> None:
    """Write top words to a file in 'word-count' format."""
    path = Path(output_filepath)
    with open(path, "w", encoding="utf-8") as f:
        for word, count in top_words:
            f.write(f"{word}-{count}\n")