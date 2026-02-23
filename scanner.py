import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

# --- CONFIGURATION ---
# Use http://localhost:8080/ for DVWA or http://localhost:3000 for Juice Shop
TARGET_URL = "http://localhost:8080" 

class WebScanner:
    def __init__(self, base_url):
        self.base_url = base_url
        self.target_links = []
        self.links_to_visit = [base_url]
        self.visited_links = set()
        self.session = requests.Session() # Useful for staying logged in later

    def extract_links_from(self, url):
        try:
            response = self.session.get(url, timeout=5)
            # Use 'html.parser' which we installed via beautifulsoup4
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup.find_all("a")
        except Exception as e:
            print(f"[-] Error accessing {url}: {e}")
            return []

    def crawl(self):
        print(f"\n--- [WebScanPro] Starting Target Scanning Module ---")
        print(f"[*] Target: {self.base_url}\n")

        while self.links_to_visit:
            url = self.links_to_visit.pop(0)

            if url not in self.visited_links:
                self.visited_links.add(url)
                print(f"[*] Exploring: {url}")

                # Find all links on the current page
                found_links = self.extract_links_from(url)
                
                for link in found_links:
                    href = link.get('href')
                    # Join relative links (e.g., /login) with the base URL
                    full_url = urljoin(self.base_url, href)

                    # Only stay on the target website; don't scan external sites like Google
                    if self.base_url in full_url and full_url not in self.visited_links:
                        # Clean the URL (remove fragment identifiers like #contact)
                        full_url = full_url.split("#")[0]
                        self.links_to_visit.append(full_url)

                # Check for forms on this page
                self.find_forms(url)
                time.sleep(0.1) # Be gentle with the server

    def find_forms(self, url):
        try:
            response = self.session.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            forms = soup.find_all("form")
            if forms:
                print(f"    [+] Found {len(forms)} form(s) on {url}")
                for form in forms:
                    action = form.get("action")
                    method = form.get("method", "get").upper()
                    print(f"        -> Action: {action} | Method: {method}")
        except:
            pass

if __name__ == "__main__":
    scanner = WebScanner(TARGET_URL)
    scanner.crawl()
    print(f"\n--- [Scan Complete] ---")
    print(f"[!] Discovered {len(scanner.visited_links)} unique pages.")