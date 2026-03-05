import requests
from bs4 import BeautifulSoup

from sqli_tester import SQLI_URL

BASE_URL = "http://127.0.0.1:8080/dvwa"
LOGIN_URL = BASE_URL + "/login.php"
XSS_URL = BASE_URL + "/vulnerabilities/xss_r/"
SECURITY_URL = BASE_URL + "/security.php"

USERNAME = "admin"
PASSWORD = "password"

def login(session):
    session.headers.update({
        "User-Agent": "Mozilla/5.0",
        "Referer": BASE_URL + "/login.php"
    })

    response = session.get(LOGIN_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    token = soup.find("input", {"name": "user_token"})["value"]

    login_data = {
        "username": USERNAME,
        "password": PASSWORD,
        "Login": "Login",
        "user_token": token
    }

    response = session.post(LOGIN_URL, data=login_data)

    if "Logout" in response.text:
        print("✅ Login Successful")
        return True
    else:
        print("❌ Login Failed")
        return False
def set_security_low(session):
    page = session.get(SECURITY_URL)
    soup = BeautifulSoup(page.text, "html.parser")
    token = soup.find("input", {"name": "user_token"})["value"]

    session.post(
        SECURITY_URL,
        data={
            "security": "low",
            "seclev_submit": "Submit",
            "user_token": token
        }
    )
    print("🔓 XSS Security set to LOW")

print("Using BASE_URL:", BASE_URL)
def run_xss_scan():
    session = requests.Session()

    if not login(session):
        return

    set_security_low(session)

    with open("xss_payloads.txt") as f:
        payloads = [p.strip() for p in f if p.strip()]

    with open("results.txt", "a", encoding="utf-8") as result_file:
        result_file.write("===== XSS Scan Results =====\n")

        for payload in payloads:

            response = session.get(XSS_URL, params={
                "name": payload,
                "Submit": "Submit"
            })

            # Always initialize status
            status = "Safe"

            # Detection Logic
            if payload in response.text:
                status = "Reflected"

            output = f"[XSS] {payload} -> {status}"
            print(output)
            result_file.write(output + "\n")

        print("✅ XSS Scan Done")