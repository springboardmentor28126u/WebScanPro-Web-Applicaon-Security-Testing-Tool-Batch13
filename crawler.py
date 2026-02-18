import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

visited_urls = set()

def crawl(start_url, max_pages=5):
    pages_to_visit = [start_url]
    count = 0

    while pages_to_visit and count < max_pages:
        url = pages_to_visit.pop(0)

        if url in visited_urls:
            continue

        print(f"\n🔍 Crawling: {url}")
        visited_urls.add(url)

        try:
            response = requests.get(url, timeout=5)
        except:
            print("❌ Cannot access page")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        # 🔹 Extract Links
        for link in soup.find_all("a", href=True):
            full_url = urljoin(url, link["href"])
            if urlparse(full_url).netloc == urlparse(start_url).netloc:
                if full_url not in visited_urls:
                    pages_to_visit.append(full_url)

        # 🔹 Extract Forms & Input Fields
        forms = soup.find_all("form")
        for form in forms:
            print("📄 Form Found")
            print(" Action:", form.get("action"))
            print(" Method:", form.get("method", "GET"))

            inputs = form.find_all(["input", "textarea", "select"])
            for field in inputs:
                print("  ➤ Input Name:", field.get("name"),
                      "| Type:", field.get("type", "text"))

        count += 1


# 🔹 Target URL (DVWA must be running)
target_url = "http://localhost/dvwa/"
crawl(target_url)
