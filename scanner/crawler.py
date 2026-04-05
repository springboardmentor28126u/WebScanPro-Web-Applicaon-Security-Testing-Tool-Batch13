import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def login_dvwa():
    session = requests.Session()

    login_url = "http://localhost/dvwa/login.php"

    response = session.get(login_url)
    soup = BeautifulSoup(response.text, "html.parser")

    user_token = soup.find("input", {"name": "user_token"})
    token_value = user_token.get("value")

    payload = {
        "username": "admin",
        "password": "password",
        "Login": "Login",
        "user_token": token_value
    }

    login_response = session.post(login_url, data=payload)

    if "Login failed" in login_response.text:
        print("[-] Login failed")
        return None
    else:
        print("[+] Logged into DVWA successfully")

    security_url = "http://localhost/dvwa/security.php"

    security_page = session.get(security_url)
    soup = BeautifulSoup(security_page.text, "html.parser")

    sec_token = soup.find("input", {"name": "user_token"}).get("value")

    security_payload = {
        "security": "low",
        "seclev_submit": "Submit",
        "user_token": sec_token
    }

    session.post(security_url, data=security_payload)

    print("[+] Security level set to LOW")

    return session


def extract_forms(url, session):
    forms_data = []

    try:
        response = session.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        forms = soup.find_all("form")

        for form in forms:
            form_info = {}

            action = form.get("action")
            full_action = urljoin(url, action) if action else url

            method = form.get("method", "get").lower()

            form_info["action"] = full_action
            form_info["method"] = method
            form_info["inputs"] = []

            for input_tag in form.find_all("input"):
                input_name = input_tag.get("name")
                input_type = input_tag.get("type", "text")

                form_info["inputs"].append({
                    "name": input_name,
                    "type": input_type
                })

            forms_data.append(form_info)

    except Exception as e:
        print(f"Error extracting forms from: {url}")
        print(e)

    return forms_data


def crawl(start_url, session, max_depth=2):
    visited = set()
    base_domain = urlparse(start_url).netloc

    results = []

    def _crawl(url, depth):
        if depth > max_depth or url in visited:
            return

        visited.add(url)

        print(f"Scanning: {url}")

        try:
            response = session.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

            # 🔥 Extract forms WITH crawling
            forms = extract_forms(url, session)

            results.append({
                "url": url,
                "forms": forms
            })

            for link in soup.find_all("a", href=True):
                full_url = urljoin(url, link["href"])
                parsed = urlparse(full_url)

                if parsed.netloc != base_domain:
                    continue

                if "logout.php" in full_url:
                    continue

                if "#" in full_url:
                    continue

                if full_url.endswith((".pdf", ".md", ".yml", ".dist")):
                    continue

                _crawl(full_url, depth + 1)

        except Exception as e:
            print("Error crawling:", url)
            print(e)

    _crawl(start_url, 0)

    return results