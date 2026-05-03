'''
Test suite for crawler.py

Test cases:

- Test successful crawl 
- Test invalid URL
- Test invalid connection 
- Test politeness delay
- Test HTTP error handling
- Test cycle detection and prevention


'''

import pytest

from src.crawler import Crawler


class DummyResponse:
	def __init__(self, text, status_code=200):
		self.text = text
		self.status_code = status_code


def test_successful_crawl(monkeypatch):
	base_url = "http://example.com/"
	page1_url = "http://example.com/page1"
	html_base = "<html><body><a href='/page1'>Next</a>Base</body></html>"
	html_page1 = "<html><body>Page One</body></html>"

	def fake_get(url):
		if url == base_url:
			return DummyResponse(html_base)
		if url == page1_url:
			return DummyResponse(html_page1)
		raise AssertionError(f"Unexpected URL: {url}")

	monkeypatch.setattr("src.crawler.requests.get", fake_get)
	monkeypatch.setattr("src.crawler.time.sleep", lambda _: None)

	crawler = Crawler(base_url=base_url)
	pages = crawler.crawl()

	assert len(pages) == 2
	assert pages[0][0] == base_url
	assert pages[1][0] == page1_url


def test_invalid_url(monkeypatch):
	base_url = "http://invalid-url/"

	def fake_get(_url):
		raise ValueError("Invalid URL")

	monkeypatch.setattr("src.crawler.requests.get", fake_get)
	monkeypatch.setattr("src.crawler.time.sleep", lambda _: None)

	crawler = Crawler(base_url=base_url)
	pages = crawler.crawl()

	assert pages == []
	assert crawler.visited_urls == set()


def test_invalid_connection(monkeypatch):
	base_url = "http://example.com/"

	class ConnectionError(Exception):
		pass

	def fake_get(_url):
		raise ConnectionError("Connection failed")

	monkeypatch.setattr("src.crawler.requests.get", fake_get)
	monkeypatch.setattr("src.crawler.time.sleep", lambda _: None)

	crawler = Crawler(base_url=base_url)
	pages = crawler.crawl()

	assert pages == []
	assert crawler.visited_urls == set()


def test_politeness_delay(monkeypatch):
	base_url = "http://example.com/"
	page1_url = "http://example.com/page1"
	html_base = "<html><body><a href='/page1'>Next</a>Base</body></html>"
	html_page1 = "<html><body>Page One</body></html>"
	sleep_calls = []

	def fake_get(url):
		if url == base_url:
			return DummyResponse(html_base)
		if url == page1_url:
			return DummyResponse(html_page1)
		raise AssertionError(f"Unexpected URL: {url}")

	def fake_sleep(seconds):
		sleep_calls.append(seconds)

	monkeypatch.setattr("src.crawler.requests.get", fake_get)
	monkeypatch.setattr("src.crawler.time.sleep", fake_sleep)

	crawler = Crawler(base_url=base_url)
	crawler.crawl()

	assert sleep_calls == [crawler.politeness_delay]


def test_http_error_handling(monkeypatch):
	base_url = "http://example.com/"

	def fake_get(_url):
		return DummyResponse("Not Found", status_code=404)

	monkeypatch.setattr("src.crawler.requests.get", fake_get)
	monkeypatch.setattr("src.crawler.time.sleep", lambda _: None)

	crawler = Crawler(base_url=base_url)
	pages = crawler.crawl()

	assert pages == []
	assert crawler.visited_urls == {base_url}


def test_cycle_detection_and_prevention(monkeypatch):
	base_url = "http://example.com/"
	page1_url = "http://example.com/page1"
	html_base = "<html><body><a href='/page1'>Next</a>Base</body></html>"
	html_page1 = "<html><body><a href='/'>Back</a>Page One</body></html>"
	called_urls = []

	def fake_get(url):
		called_urls.append(url)
		if url == base_url:
			return DummyResponse(html_base)
		if url == page1_url:
			return DummyResponse(html_page1)
		raise AssertionError(f"Unexpected URL: {url}")

	monkeypatch.setattr("src.crawler.requests.get", fake_get)
	monkeypatch.setattr("src.crawler.time.sleep", lambda _: None)

	crawler = Crawler(base_url=base_url)
	pages = crawler.crawl()

	assert len(pages) == 2
	assert called_urls.count(base_url) == 1
	assert called_urls.count(page1_url) == 1