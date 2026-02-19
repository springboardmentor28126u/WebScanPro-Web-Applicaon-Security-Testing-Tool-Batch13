import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import os

START_URL = "http://localhost/DVWA/"
visited_urls = set()
metadata = []

session = requests.Session()  # Better for handling cookies


def is_same_domain(url):
    return urlparse(url).netloc == urlparse(START_URL).netloc


def extract_forms(soup, url):
    forms_data = []

    for form in soup.find_all("form"):
        action = form.get("action")
        if action:
            action = urljoin(url, action)
        else:
            action = url  # If action is None, submit to same page

        form_details = {
            "action": action,
            "method": form.get("method", "get").lower(),
            "inputs": []
        }

        for input_tag in form.find_all("input"):
            input_details = {
                "type": input_tag.get("type", "text"),
                "name": input_tag.get("name"),
                "value": input_tag.get("value", "")
            }
            form_details["inputs"].append(input_details)

        forms_data.append(form_details)

    return forms_data


def crawl(url):
    if url in visited_urls:
        return

    print(f"[+] Crawling: {url}")
    visited_urls.add(url)

    try:
        response = session.get(url, timeout=5)

        # Only process valid pages
        if response.status_code != 200:
            return

    except requests.exceptions.RequestException as e:
        print(f"[!] Failed to access {url}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    forms = extract_forms(soup, url)

    page_data = {
        "url": url,
        "forms": forms
    }

    metadata.append(page_data)

    for link in soup.find_all("a"):
        href = link.get("href")

        if href:
            full_url = urljoin(url, href)

            if is_same_domain(full_url):
                crawl(full_url)


def save_metadata():
    os.makedirs("output", exist_ok=True)

    with open("output/metadata.json", "w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=4)

    print("\n[✔] Metadata saved to output/metadata.json")


if __name__ == "__main__":
    crawl(START_URL)
    save_metadata()
if __name__ == "__main__":
    crawl(START_URL)
    print(f"\nTotal URLs Found: {len(visited_urls)}")   
    save_metadata()
