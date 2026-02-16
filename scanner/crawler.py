import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Create session to maintain login cookies
session = requests.Session()
visited = set()


def login_dvwa():
    login_url = "http://localhost/dvwa/login.php"

    # Step 1: Get login page and extract CSRF token
    response = session.get(login_url)
    soup = BeautifulSoup(response.text, "html.parser")

    user_token = soup.find("input", {"name": "user_token"})
    token_value = user_token.get("value")

    # Step 2: Send login request
    payload = {
        "username": "admin",
        "password": "password",
        "Login": "Login",
        "user_token": token_value
    }

    login_response = session.post(login_url, data=payload)

    if "Login failed" in login_response.text:
        print("[-] Login failed")
        return
    else:
        print("[+] Logged into DVWA successfully")

    # Step 3: Set security level to LOW
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


def crawl(url, base_domain):
    if url in visited:
        return []

    visited.add(url)
    links_found = []

    try:
        response = session.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        for link in soup.find_all("a", href=True):
            full_url = urljoin(url, link['href'])
            parsed = urlparse(full_url)

            # Stay inside same domain
            if parsed.netloc != base_domain:
                continue
            # Ignore logout page
            if "logout.php" in full_url:
                continue


            # Ignore anchors
            if "#" in full_url:
                continue

            # Ignore unwanted file types
            if full_url.endswith((".pdf", ".md", ".yml", ".dist")):
                continue

            links_found.append(full_url)

        return links_found

    except Exception as e:
        print("Error crawling:", url)
        return []
