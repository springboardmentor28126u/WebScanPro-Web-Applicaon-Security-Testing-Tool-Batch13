import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import os

# ---------------- CONFIG ---------------- #

BASE_URL = "http://localhost/dvwa/"
LOGIN_URL = urljoin(BASE_URL, "login.php")
MAX_DEPTH = 3   # Prevent infinite crawling

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_JSON = os.path.join(BASE_DIR, "output.json")
OUTPUT_TXT = os.path.join(BASE_DIR, "output.txt")

visited = set()
session = requests.Session()

results = {
    "urls": [],
    "forms": []
}

# ---------------- LOGIN FUNCTION ---------------- #

def login_dvwa():
    print("[+] Logging into DVWA for crawling...")

    response = session.get(LOGIN_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    token_input = soup.find("input", {"name": "user_token"})
    user_token = token_input["value"] if token_input else ""

    login_data = {
        "username": "admin",
        "password": "password",
        "Login": "Login",
        "user_token": user_token
    }

    session.post(LOGIN_URL, data=login_data)
    print("[+] Login successful.")


# ---------------- CRAWLER ---------------- #

def crawl(url, depth=0):

    if depth > MAX_DEPTH:
        return

    if url in visited:
        return

    visited.add(url)

    try:
        response = session.get(url, timeout=5)

        if response.status_code != 200:
            return

    except requests.RequestException:
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # -------- Store URL Metadata --------
    results["urls"].append({
        "url": url,
        "status_code": response.status_code,
        "content_length": len(response.text),
        "title": soup.title.string.strip() if soup.title else ""
    })

    # -------- Extract Links --------
    for link in soup.find_all("a"):
        href = link.get("href")
        if not href:
            continue

        full_url = urljoin(url, href)
        full_url = full_url.split("#")[0]

        # Skip logout & external
        if BASE_URL not in full_url:
            continue
        if "logout" in full_url.lower():
            continue

        crawl(full_url, depth + 1)

    # -------- Extract Forms --------
    for form in soup.find_all("form"):

        action = form.get("action")
        action = urljoin(url, action) if action else url
        action = action.split("#")[0]

        method = form.get("method", "get").lower()

        form_details = {
            "page": url,
            "action": action,
            "method": method,
            "inputs": []
        }

        for input_tag in form.find_all("input"):
            name = input_tag.get("name")
            if not name:
                continue

            form_details["inputs"].append({
                "name": name,
                "type": input_tag.get("type", "text"),
                "value": input_tag.get("value", "")
            })

        # Avoid duplicate forms
        if form_details["inputs"] and form_details not in results["forms"]:
            results["forms"].append(form_details)


# ---------------- MAIN ---------------- #

if __name__ == "__main__":

    login_dvwa()
    crawl(BASE_URL)

    print(f"[+] Total URLs Discovered: {len(results['urls'])}")
    print(f"[+] Total Forms Discovered: {len(results['forms'])}")

    with open(OUTPUT_JSON, "w") as jf:
        json.dump(results, jf, indent=4)

    with open(OUTPUT_TXT, "w") as tf:
        tf.write("=== Discovered URLs ===\n")
        for u in results["urls"]:
            tf.write(str(u) + "\n")

        tf.write("\n=== Forms & Input Fields ===\n")
        for f in results["forms"]:
            tf.write(str(f) + "\n")

    print("Scan completed. Results saved in Week-2/output.txt and Week-2/output.json.")