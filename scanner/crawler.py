# scanner/crawler.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from scanner.config import TARGET_URL

# URLs to never visit during crawl
BLACKLIST = ['logout', 'setup.php', 'phpinfo', 'ids_log']

def crawl(base_url, session, max_pages=50):
    visited = set()
    to_visit = [base_url]
    results = []

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue

        # Skip blacklisted URLs
        if any(bl in url for bl in BLACKLIST):
            print(f"  Skipping: {url}")
            continue

        try:
            resp = session.get(url, timeout=5)
            visited.add(url)

            # If redirected to login, session expired — stop
            if 'login.php' in resp.url:
                print(f"  [WARN] Session expired at {url}")
                break

            soup = BeautifulSoup(resp.text, 'html.parser')

            for link in soup.find_all('a', href=True):
                full = urljoin(base_url, link['href'])
                if urlparse(full).netloc == urlparse(base_url).netloc:
                    to_visit.append(full)

            forms = []
            for form in soup.find_all('form'):
                inputs = [i.get('name') for i in form.find_all('input')]
                forms.append({
                    'action': urljoin(url, form.get('action', '')),
                    'method': form.get('method', 'get').upper(),
                    'inputs': inputs
                })

            results.append({'url': url, 'forms': forms})
            print(f"  Crawled: {url}")

        except Exception as e:
            print(f"  Error: {url} -> {e}")

    return results