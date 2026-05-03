''''
Test suite for indexer.py

Test cases:

BUILD:
- Test building index from sample data
- Test with empty data
- Test with duplicate words in the same page
- Test with special characters and mixed case
- Test with stop words
- Test saving index
- Test invalid directory for saving index

LOAD:
- Test successful load of index
- Test invalid file path
- Test loading empty index file
- Test loading index file with invalid format

GET INDEX:
- Test get_index returns the correct structure
'''

import json

import pytest

from src.indexer import Indexer


def test_build_index_from_sample_data():
	indexer = Indexer()
	pages = [
		("http://a.com", "Hello world"),
		("http://b.com", "Hello there world"),
	]

	indexer.build_index(pages)
	index = indexer.get_index()

	assert set(index["hello"]) == {"http://a.com", "http://b.com"}
	assert set(index["world"]) == {"http://a.com", "http://b.com"}
	assert set(index["there"]) == {"http://b.com"}


def test_build_index_with_empty_data():
	indexer = Indexer()

	indexer.build_index([])

	assert indexer.get_index() == {}


def test_build_index_with_duplicate_words_same_page():
	indexer = Indexer()
	pages = [("http://a.com", "hello hello hello")]

	indexer.build_index(pages)
	index = indexer.get_index()

	assert index["hello"] == ["http://a.com"]


def test_build_index_with_special_characters_and_mixed_case():
	indexer = Indexer()
	pages = [("http://a.com", "Hello, WORLD!! C++")]

	indexer.build_index(pages)
	index = indexer.get_index()

	assert set(index.keys()) == {"hello", "world", "c"}


def test_build_index_with_stop_words():
	indexer = Indexer()
	pages = [("http://a.com", "the and of")]

	indexer.build_index(pages)
	index = indexer.get_index()

	assert set(index.keys()) == {"the", "and", "of"}


def test_save_index_creates_file(tmp_path):
	index_file = tmp_path / "index.json"
	indexer = Indexer(index_file=str(index_file))
	pages = [("http://a.com", "hello world")]

	indexer.build_index(pages)
	indexer.save()

	assert index_file.exists()
	with index_file.open("r", encoding="utf-8") as f:
		saved = json.load(f)
	assert saved == {"hello": ["http://a.com"], "world": ["http://a.com"]}


def test_save_index_invalid_directory(tmp_path):
	not_a_dir = tmp_path / "not_a_dir"
	not_a_dir.write_text("x", encoding="utf-8")
	index_file = not_a_dir / "index.json"
	indexer = Indexer(index_file=str(index_file))
	pages = [("http://a.com", "hello world")]

	indexer.build_index(pages)

	with pytest.raises(OSError):
		indexer.save()


def test_load_index_successful(tmp_path):
	index_file = tmp_path / "index.json"
	indexer = Indexer(index_file=str(index_file))
	pages = [("http://a.com", "hello world")]
	indexer.build_index(pages)
	indexer.save()

	new_indexer = Indexer(index_file=str(index_file))

	assert new_indexer.load() is True
	assert new_indexer.get_index() == {"hello": ["http://a.com"], "world": ["http://a.com"]}


def test_load_index_invalid_file_path(tmp_path):
	index_file = tmp_path / "missing.json"
	indexer = Indexer(index_file=str(index_file))

	assert indexer.load() is False


def test_load_empty_index_file(tmp_path):
	index_file = tmp_path / "index.json"
	index_file.write_text("", encoding="utf-8")
	indexer = Indexer(index_file=str(index_file))

	assert indexer.load() is False


def test_load_invalid_format_index_file(tmp_path):
	index_file = tmp_path / "index.json"
	index_file.write_text("{", encoding="utf-8")
	indexer = Indexer(index_file=str(index_file))

	assert indexer.load() is False


def test_get_index_returns_structure():
	indexer = Indexer()
	pages = [("http://a.com", "hello world")]

	indexer.build_index(pages)
	index = indexer.get_index()

	assert index == {"hello": ["http://a.com"], "world": ["http://a.com"]}

