import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

# ---------------- CONFIG ---------------- #

BASE_URL = "http://localhost/dvwa/"
LOGIN_URL = urljoin(BASE_URL, "login.php")

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
def crawl(url):
    if url in visited:
        return

    visited.add(url)

    try:
        response = session.get(url, timeout=5)
    except:
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # ---- Extract Links ----
    for link in soup.find_all("a"):
        href = link.get("href")
        if href:
            full_url = urljoin(url, href)

            if BASE_URL in full_url and full_url not in results["urls"]:
                results["urls"].append(full_url)
                crawl(full_url)

    # ---- Extract Forms ----
    for form in soup.find_all("form"):

        form_details = {}

        action = form.get("action")
        method = form.get("method", "get").lower()

        form_details["page"] = url
        form_details["action"] = urljoin(url, action) if action else url
        form_details["method"] = method
        form_details["inputs"] = []

        for input_tag in form.find_all("input"):
            input_info = {
                "name": input_tag.get("name"),
                "type": input_tag.get("type", "text"),
                "value": input_tag.get("value", "")
            }
            form_details["inputs"].append(input_info)

        results["forms"].append(form_details)

# ---------------- MAIN ---------------- #
if __name__ == "__main__":

    login_dvwa()
    crawl(BASE_URL)

    print(f"[+] Total URLs Discovered: {len(results['urls'])}")
    print(f"[+] Total Forms Discovered: {len(results['forms'])}")

    with open("output.json", "w") as jf:
        json.dump(results, jf, indent=4)

    with open("output.txt", "w") as tf:
        tf.write("=== Discovered URLs ===\n")
        for u in results["urls"]:
            tf.write(u + "\n")

        tf.write("\n=== Forms & Input Fields ===\n")
        for f in results["forms"]:
            tf.write(str(f) + "\n")

    

print("Scan completed. Results saved to output.txt")
