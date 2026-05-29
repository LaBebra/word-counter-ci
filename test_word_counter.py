"""
Unit tests for word_counter.py using pytest.
Uses fixtures and parametrization as required.
"""

import pytest
from collections import Counter

from word_counter import (
    read_file,
    extract_words,
    count_words,
    get_top_words,
    write_results,
    process_file,
)


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def sample_text():
    """Return a simple sample text for testing."""
    return (
        "the quick brown fox jumps over the lazy dog "
        "the fox was very quick and the dog was very lazy"
    )


@pytest.fixture
def sample_words(sample_text):
    """Return extracted words from sample_text."""
    return extract_words(sample_text)


@pytest.fixture
def sample_counter(sample_words):
    """Return a Counter from sample_words."""
    return count_words(sample_words)


@pytest.fixture
def txt_file(tmp_path):
    """Create a temporary .txt file with known content."""
    content = (
        "apple banana apple cherry banana apple "
        "date cherry banana apple date date cherry "
        "elderberry fig apple banana grape grape grape"
    )
    file = tmp_path / "test_input.txt"
    file.write_text(content, encoding="utf-8")
    return file


@pytest.fixture
def non_txt_file(tmp_path):
    """Create a temporary non-.txt file."""
    file = tmp_path / "test_input.csv"
    file.write_text("hello,world", encoding="utf-8")
    return file


@pytest.fixture
def output_file(tmp_path):
    """Return a path for the output file."""
    return tmp_path / "output.txt"


# ── Tests for read_file ────────────────────────────────────────────────────────

class TestReadFile:

    def test_reads_existing_txt_file(self, txt_file):
        content = read_file(str(txt_file))
        assert "apple" in content
        assert "banana" in content

    def test_raises_for_missing_file(self, tmp_path):
        missing = tmp_path / "nonexistent.txt"
        with pytest.raises(FileNotFoundError):
            read_file(str(missing))

    def test_raises_for_wrong_extension(self, non_txt_file):
        with pytest.raises(ValueError, match=r"\.txt"):
            read_file(str(non_txt_file))

    def test_returns_string(self, txt_file):
        result = read_file(str(txt_file))
        assert isinstance(result, str)


# ── Tests for extract_words ────────────────────────────────────────────────────

class TestExtractWords:

    @pytest.mark.parametrize("text, expected_contains", [
        ("Hello World", ["hello", "world"]),
        ("Python is great!", ["python", "is", "great"]),
        ("один два три", ["один", "два", "три"]),
        ("test, test. test!", ["test", "test", "test"]),
    ])
    def test_extracts_words_correctly(self, text, expected_contains):
        result = extract_words(text)
        for word in expected_contains:
            assert word in result

    @pytest.mark.parametrize("text, not_expected", [
        ("hello, world!", [",", "!", ".", " "]),
        ("test123 foo", ["123"]),
    ])
    def test_excludes_punctuation_and_digits(self, text, not_expected):
        result = extract_words(text)
        for item in not_expected:
            assert item not in result

    def test_returns_lowercase(self, sample_text):
        result = extract_words(sample_text)
        for word in result:
            assert word == word.lower()

    def test_empty_text_returns_empty_list(self):
        result = extract_words("")
        assert result == []

    def test_returns_list(self, sample_text):
        result = extract_words(sample_text)
        assert isinstance(result, list)


# ── Tests for count_words ──────────────────────────────────────────────────────

class TestCountWords:

    def test_returns_counter(self, sample_words):
        result = count_words(sample_words)
        assert isinstance(result, Counter)

    def test_counts_correctly(self):
        words = ["a", "b", "a", "c", "a", "b"]
        result = count_words(words)
        assert result["a"] == 3
        assert result["b"] == 2
        assert result["c"] == 1

    def test_empty_list_returns_empty_counter(self):
        result = count_words([])
        assert result == Counter()

    @pytest.mark.parametrize("words, word, expected_count", [
        (["apple", "apple", "banana"], "apple", 2),
        (["apple", "apple", "banana"], "banana", 1),
        (["apple", "apple", "banana"], "cherry", 0),
    ])
    def test_specific_word_counts(self, words, word, expected_count):
        result = count_words(words)
        assert result[word] == expected_count


# ── Tests for get_top_words ────────────────────────────────────────────────────

class TestGetTopWords:

    def test_returns_list(self, sample_counter):
        result = get_top_words(sample_counter)
        assert isinstance(result, list)

    def test_default_returns_10(self, sample_counter):
        result = get_top_words(sample_counter)
        assert len(result) <= 10

    @pytest.mark.parametrize("n", [1, 3, 5, 10])
    def test_respects_n_parameter(self, sample_counter, n):
        result = get_top_words(sample_counter, n)
        assert len(result) <= n

    def test_raises_for_invalid_n(self, sample_counter):
        with pytest.raises(ValueError):
            get_top_words(sample_counter, 0)
        with pytest.raises(ValueError):
            get_top_words(sample_counter, -1)

    def test_sorted_by_frequency_descending(self, sample_counter):
        result = get_top_words(sample_counter, 5)
        counts = [count for _, count in result]
        assert counts == sorted(counts, reverse=True)

    def test_result_contains_tuples(self, sample_counter):
        result = get_top_words(sample_counter, 3)
        for item in result:
            assert isinstance(item, tuple)
            assert len(item) == 2


# ── Tests for write_results ────────────────────────────────────────────────────

class TestWriteResults:

    def test_creates_output_file(self, output_file):
        write_results([("apple", 5), ("banana", 3)], str(output_file))
        assert output_file.exists()

    def test_correct_format(self, output_file):
        top_words = [("apple", 5), ("banana", 3)]
        write_results(top_words, str(output_file))
        lines = output_file.read_text(encoding="utf-8").strip().split("\n")
        assert lines[0] == "apple-5"
        assert lines[1] == "banana-3"

    def test_correct_number_of_lines(self, output_file):
        top_words = [("a", 3), ("b", 2), ("c", 1)]
        write_results(top_words, str(output_file))
        lines = output_file.read_text(encoding="utf-8").strip().split("\n")
        assert len(lines) == 3

    @pytest.mark.parametrize("top_words,expected_lines", [
        ([("hello", 7)], ["hello-7"]),
        ([("x", 1), ("y", 2)], ["x-1", "y-2"]),
        ([], []),
    ])
    def test_various_inputs(self, tmp_path, top_words, expected_lines):
        out = tmp_path / "out.txt"
        write_results(top_words, str(out))
        content = out.read_text(encoding="utf-8").strip()
        if expected_lines:
            lines = content.split("\n")
            assert lines == expected_lines
        else:
            assert content == ""


# ── Tests for process_file (integration) ──────────────────────────────────────

class TestProcessFile:

    def test_returns_list_of_tuples(self, txt_file, output_file):
        result = process_file(str(txt_file), str(output_file))
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, tuple)

    def test_creates_output_file(self, txt_file, output_file):
        process_file(str(txt_file), str(output_file))
        assert output_file.exists()

    def test_top_word_is_most_frequent(self, txt_file, output_file):
        # 'apple' appears 5 times in txt_file fixture
        result = process_file(str(txt_file), str(output_file))
        top_word = result[0][0]
        assert top_word == "apple"

    def test_output_file_has_correct_format(self, txt_file, output_file):
        process_file(str(txt_file), str(output_file))
        lines = output_file.read_text(encoding="utf-8").strip().split("\n")
        for line in lines:
            assert "-" in line
            parts = line.rsplit("-", 1)
            assert len(parts) == 2
            assert parts[1].isdigit()

    def test_respects_top_n_parameter(self, txt_file, output_file):
        result = process_file(str(txt_file), str(output_file), top_n=3)
        assert len(result) <= 3

    def test_raises_for_missing_file(self, tmp_path, output_file):
        missing = tmp_path / "missing.txt"
        with pytest.raises(FileNotFoundError):
            process_file(str(missing), str(output_file))
