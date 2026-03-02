from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

visited_urls = set()


def crawl(url, session):
    if url in visited_urls:
        return []

    print(f"[+] crawling: {url}")
    visited_urls.add(url)
    forms_found = []

    response = session.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    for form in soup.find_all("form"):
        form_details = {
            "action": urljoin(url, form.get("action")),
            "method": form.get("method", "get").lower(),
            "inputs": []
        }

        for input_tag in form.find_all("input"):
            form_details["inputs"].append({
                "name": input_tag.get("name"),
                "type": input_tag.get("type", "text")
            })

        forms_found.append(form_details)

    for link in soup.find_all("a"):
        href = link.get("href")
        if href:
            full_url = urljoin(url, href)
            if urlparse(full_url).netloc == urlparse(url).netloc:
                forms_found.extend(crawl(full_url, session))

    return forms_found