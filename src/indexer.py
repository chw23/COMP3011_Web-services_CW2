import json
import os
import re
from collections import defaultdict

class Indexer:
    def __init__(self, index_file='data/index.json'):
        self.index_file = index_file
        self.inverted_index = defaultdict(list)
        
    def build_index(self, pages_data):
        self.inverted_index.clear()
        for url, text in pages_data:
            # Tokenize and lowercase
            words = re.findall(r'\b\w+\b', text.lower())
            
            # Use a set to avoid duplicate URLs for the same word on the same page
            unique_words = set(words)
            
            for word in unique_words:
                self.inverted_index[word].append(url)
        print("Index built successfully.")
                
    def save(self):
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.index_file), exist_ok=True)
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(self.inverted_index, f, indent=4)
        print(f"Index successfully saved to {self.index_file}.")
        
    def load(self):
        if not os.path.exists(self.index_file):
            print(f"Error: Index file '{self.index_file}' not found. Please run 'build' first.")
            return False
            
        try:
            with open(self.index_file, 'r', encoding='utf-8') as f:
                self.inverted_index = json.load(f)
            print(f"Index successfully loaded from {self.index_file}.")
            return True
        except Exception as e:
            print(f"Error loading index: {e}")
            return False
            
    def get_index(self):
        return self.inverted_index
