import sys
import os
from crawler import Crawler
from indexer import Indexer
from search import Searcher

def main():
    # Make sure we write to the right data directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data', 'index.json')
    
    indexer = Indexer(index_file=data_dir)
    searcher = Searcher(indexer)
    
    print("Welcome to the Web Search CLI!")
    print("Available commands:")
    print("  build            - Crawl quotes.toscrape.com and build the index")
    print("  load             - Load the index file from /data/index.json")
    print("  print <word>     - Print the inverted index for a particular word")
    print("  find <phrase>    - Find a given query phrase in the index")
    print("  quit / exit      - Exit the application")
    
    while True:
        try:
            user_input = input("\n> ").strip()
            if not user_input:
                continue
                
            parts = user_input.split(maxsplit=1)
            cmd = parts[0].lower()
            arg = parts[1] if len(parts) > 1 else ""
            
            if cmd in ['quit', 'exit']:
                print("Goodbye!")
                break
            elif cmd == 'build':
                print("Starting crawler (This will take a while due to politeness window)...")
                crawler = Crawler()
                pages_data = crawler.crawl()
                indexer.build_index(pages_data)
                indexer.save()
            elif cmd == 'load':
                indexer.load()
            elif cmd == 'print':
                if not arg:
                    print("Usage: print <word>")
                    continue
                searcher.print_word(arg)
            elif cmd == 'find':
                if not arg:
                    print("Usage: find <phrase>")
                    continue
                searcher.find_phrase(arg)
            else:
                print(f"Unknown command: {cmd}")
        except KeyboardInterrupt:
            print("\nOperation cancelled. Type 'exit' to quit.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
