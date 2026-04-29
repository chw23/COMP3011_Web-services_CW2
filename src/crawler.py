import time
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

class Crawler:
    def __init__(self, base_url="https://quotes.toscrape.com/"):
        self.base_url = base_url
        self.visited_urls = set()
        self.pages_data = [] # List of tuples: (url, text)
        self.politeness_delay = 6

    def crawl(self):
        url_queue = [self.base_url]
        
        while url_queue:
            current_url = url_queue.pop(0)
            if current_url in self.visited_urls:
                continue
                
            print(f"Crawling: {current_url}")
            try:
                response = requests.get(current_url)
                self.visited_urls.add(current_url)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    # Extract text
                    text = soup.get_text(separator=' ', strip=True)
                    self.pages_data.append((current_url, text))
                    
                    # Find next links
                    for link in soup.find_all('a', href=True):
                        href = link.get('href')
                        full_url = urljoin(self.base_url, href)
                        # Keep crawling on quotes.toscrape.com
                        if full_url.startswith(self.base_url) and full_url not in self.visited_urls and full_url not in url_queue:
                            url_queue.append(full_url)
            except Exception as e:
                print(f"Failed to crawl {current_url}: {e}")
            
            if url_queue:
                print(f"Waiting {self.politeness_delay} seconds for politeness...")
                time.sleep(self.politeness_delay)
                
        return self.pages_data
