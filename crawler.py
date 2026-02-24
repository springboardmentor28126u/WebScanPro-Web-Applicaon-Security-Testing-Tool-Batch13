from bs4 import BeautifulSoup
from urllib.parse import urljoin

def crawl(start_url, requester, max_depth=2):

    visited = set()
    queue = [(start_url, 0)]
    discovered = []

    while queue:
        url, depth = queue.pop(0)

        if url in visited or depth > max_depth:
            continue

        print(f"Crawling: {url}")

        visited.add(url)

        try:
            response = requester.session.get(url, timeout=5)
            soup = BeautifulSoup(response.text, "html.parser")

            discovered.append(url)

            for link in soup.find_all("a", href=True):
                full_url = urljoin(url, link["href"])

                if "localhost" in full_url:
                    queue.append((full_url, depth + 1))

        except:
            pass

    return discovered
