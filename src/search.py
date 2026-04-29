import re

class Searcher:
    def __init__(self, indexer):
        self.indexer = indexer
        
    def print_word(self, word):
        index = self.indexer.get_index()
        word = word.lower()
        if not index:
            print("Error: Index is empty. Please load or build the index first.")
            return
            
        urls = index.get(word, [])
        if urls:
            print(f"Word '{word}' found in {len(urls)} pages:")
            for url in urls:
                print(f" - {url}")
        else:
            print(f"Word '{word}' not found in the index.")
            
    def find_phrase(self, phrase):
        index = self.indexer.get_index()
        if not index:
            print("Error: Index is empty. Please load or build the index first.")
            return
            
        words = list(set(re.findall(r'\b\w+\b', phrase.lower())))
        if not words:
            print("Invalid phrase.")
            return
            
        common_urls = set(index.get(words[0], []))
        
        for word in words[1:]:
            common_urls.intersection_update(index.get(word, []))
            
        if common_urls:
            print(f"Phrase '{phrase}' found in {len(common_urls)} pages:")
            for url in common_urls:
                print(f" - {url}")
        else:
            print(f"Phrase '{phrase}' not found in any single page in the index.")
