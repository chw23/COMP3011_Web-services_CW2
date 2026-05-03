'''
Test suite for search.py

PRINT WORD:
- Test printing a word that exists in the index
- Test printing a word that does not exist in the index
- Test printing a word when the index is empty

FIND PHRASE:
- Test finding a phrase that exists in the index
- Test finding a phrase that does not exist in the index
- Test finding a phrase when the index is empty
- Test finding a phrase with words that exist but not on the same page
- Test finding a phrase with duplicate words
- Test finding a phrase with special characters
- Test finding a phrase with mixed case
- Test finding a phrase with leading/trailing whitespace
'''

import pytest

from src.search import Searcher


class DummyIndexer:
	def __init__(self, index):
		self._index = index

	def get_index(self):
		return self._index


def test_print_word_exists(capsys):
	indexer = DummyIndexer({"hello": ["http://a.com", "http://b.com"]})
	searcher = Searcher(indexer)

	searcher.print_word("hello")
	output = capsys.readouterr().out

	assert "Word 'hello' found in 2 pages:" in output
	assert "http://a.com" in output
	assert "http://b.com" in output


def test_print_word_not_exists(capsys):
	indexer = DummyIndexer({"hello": ["http://a.com"]})
	searcher = Searcher(indexer)

	searcher.print_word("missing")
	output = capsys.readouterr().out

	assert "Word 'missing' not found in the index." in output


def test_print_word_empty_index(capsys):
	indexer = DummyIndexer({})
	searcher = Searcher(indexer)

	searcher.print_word("hello")
	output = capsys.readouterr().out

	assert "Error: Index is empty. Please load or build the index first." in output


def test_find_phrase_exists(capsys):
	indexer = DummyIndexer({
		"hello": ["http://a.com", "http://b.com"],
		"world": ["http://a.com"],
	})
	searcher = Searcher(indexer)

	searcher.find_phrase("hello world")
	output = capsys.readouterr().out

	assert "Phrase 'hello world' found in 1 pages:" in output
	assert "http://a.com" in output


def test_find_phrase_not_exists(capsys):
	indexer = DummyIndexer({
		"hello": ["http://a.com"],
		"world": ["http://a.com"],
	})
	searcher = Searcher(indexer)

	searcher.find_phrase("hello missing")
	output = capsys.readouterr().out

	assert "Phrase 'hello missing' not found in any single page in the index." in output


def test_find_phrase_empty_index(capsys):
	indexer = DummyIndexer({})
	searcher = Searcher(indexer)

	searcher.find_phrase("hello world")
	output = capsys.readouterr().out

	assert "Error: Index is empty. Please load or build the index first." in output


def test_find_phrase_words_not_on_same_page(capsys):
	indexer = DummyIndexer({
		"hello": ["http://a.com"],
		"world": ["http://b.com"],
	})
	searcher = Searcher(indexer)

	searcher.find_phrase("hello world")
	output = capsys.readouterr().out

	assert "Phrase 'hello world' not found in any single page in the index." in output


def test_find_phrase_with_duplicate_words(capsys):
	indexer = DummyIndexer({"hello": ["http://a.com", "http://b.com"]})
	searcher = Searcher(indexer)

	searcher.find_phrase("hello hello")
	output = capsys.readouterr().out

	assert "Phrase 'hello hello' found in 2 pages:" in output
	assert "http://a.com" in output
	assert "http://b.com" in output


def test_find_phrase_with_special_characters(capsys):
	indexer = DummyIndexer({
		"hello": ["http://a.com"],
		"world": ["http://a.com"],
	})
	searcher = Searcher(indexer)

	searcher.find_phrase("hello!!! world??")
	output = capsys.readouterr().out

	assert "Phrase 'hello!!! world??' found in 1 pages:" in output
	assert "http://a.com" in output


def test_find_phrase_with_mixed_case(capsys):
	indexer = DummyIndexer({
		"hello": ["http://a.com"],
		"world": ["http://a.com"],
	})
	searcher = Searcher(indexer)

	searcher.find_phrase("HeLLo WoRld")
	output = capsys.readouterr().out

	assert "Phrase 'HeLLo WoRld' found in 1 pages:" in output
	assert "http://a.com" in output


def test_find_phrase_with_leading_trailing_whitespace(capsys):
	indexer = DummyIndexer({
		"hello": ["http://a.com"],
		"world": ["http://a.com"],
	})
	searcher = Searcher(indexer)

	searcher.find_phrase("  hello world  ")
	output = capsys.readouterr().out

	assert "Phrase '  hello world  ' found in 1 pages:" in output
	assert "http://a.com" in output