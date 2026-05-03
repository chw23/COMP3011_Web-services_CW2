# COMP3011_Web-services_CW2

## Project Overview and Purpose

This project utilises the Crawler python package to demonstrate a simple and polite way of web crawling on https://quotes.toscrape.com. A CLI is implemented for the operation of the software.

### Directory Structure

* `data/`: Contains the inverted index once it has been built.
* `src/`: Code of all core components can be found here.
* `tests/`: Includes test suites for testing the core components.

## Installation Instructions

1. Navigate to the root directory of the project.
2. Create a virtual environment (if you don't have one):
   ```bash
   python3 -m venv .venv
   ```
3. Activate the virtual environment:
   * **macOS/Linux:** `source .venv/bin/activate`
   * **Windows:** `.\.venv\Scripts\activate`
4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage Examples

Run the application (e.g., using `python src/main.py`) to launch the CLI. Inside the CLI, you can run the following commands:

* `build`
  Crawl on quotes.toscrape.com and build an inverted index of all word occurrences in the pages of the website.

* `load`
  Load the index file from `data/`. **This operation is only allowed after an index file is built!**

* `print <word>`
  Print out the inverted index of a particular word.

* `find <phrase>`
  Find the index of pages that contains the phrase.

* `quit` / `exit`
  Quit the application.

## Testing Instructions

This project uses `pytest` for testing the core components located in `tests/`. 
To run all test suites, ensure your virtual environment is activated and simply execute:
```bash
pytest
```
```