import requests
from bs4 import BeautifulSoup

# Common passwords attackers try first
COMMON_PASSWORDS = ["password", "123456", "admin", "letmein", "qwerty", "password1"]

def brute_force(login_url, username, passwords=COMMON_PASSWORDS):
    findings = []

    for pwd in passwords:
        session = requests.Session()

        # Step 1: Get login page
        r = session.get(login_url)
        soup = BeautifulSoup(r.text, "html.parser")

        token_tag = soup.find("input", {"name": "user_token"})
        token = token_tag["value"] if token_tag else ""

        # Step 2: Send login request
        payload = {
            "username": username,
            "password": pwd,
            "Login": "Login",
            "user_token": token
        }

        resp = session.post(login_url, data=payload)

        # Success indicator
        if "Username and/or password incorrect." not in resp.text:
            findings.append({
                "username": username,
                "password": pwd,
                "type": "Weak Credentials",
                "severity": "HIGH",
                "url": login_url,
                "parameter": "password",
                "payload": pwd
            })

            print(f"  [VULN] Weak credentials: {username}:{pwd}")
            break

        else:
            print(f"  Tried {username}:{pwd} - failed")

    return findings

def check_cookie_security(session, url):
    session.get(url)
    issues = []
    for cookie in session.cookies:
        # Secure flag — cookie only sent over HTTPS, not plain HTTP
        if not cookie.secure:
            issues.append({'type': 'Insecure Cookie', 'parameter': cookie.name,
                           'payload': 'Missing Secure flag', 'url': url,
                           'issue': 'Missing Secure flag', 'severity': 'MEDIUM'})
        # HttpOnly flag — cookie cannot be read by JavaScript (prevents XSS theft)
        if not cookie.has_nonstandard_attr('HttpOnly'):
            issues.append({'type': 'Insecure Cookie', 'parameter': cookie.name,
                           'payload': 'Missing HttpOnly flag', 'url': url,
                           'issue': 'Missing HttpOnly flag', 'severity': 'MEDIUM'})
    return issues