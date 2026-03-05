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


def crawl(url, base_domain, session, visited):
    if url in visited:
        return []

    visited.add(url)
    links_found = []

    try:
        response = session.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

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

            links_found.append(full_url)

    except Exception as e:
        print("Error crawling:", url)
        print(e)

    return links_found