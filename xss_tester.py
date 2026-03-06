import requests
import json
from bs4 import BeautifulSoup
from xss_payloads import XSS_PAYLOADS

session = requests.Session()
results = []

def login_dvwa():
    login_url = "http://localhost/dvwa/login.php"

    response = session.get(login_url)
    soup = BeautifulSoup(response.text, "html.parser")

    user_token = soup.find("input", {"name": "user_token"})["value"]

    login_data = {
        "username": "admin",
        "password": "password",
        "Login": "Login",
        "user_token": user_token
    }

    session.post(login_url, data=login_data)
    print("Logged into DVWA successfully.\n")


def set_security_low():
    security_url = "http://localhost/dvwa/security.php"

    response = session.get(security_url)
    soup = BeautifulSoup(response.text, "html.parser")

    user_token = soup.find("input", {"name": "user_token"})["value"]

    security_data = {
        "security": "low",
        "seclev_submit": "Submit",
        "user_token": user_token
    }

    session.post(security_url, data=security_data)
    print("DVWA Security level set to LOW.\n")


def test_xss(url):
    print("Starting XSS Scan...\n")

    for payload in XSS_PAYLOADS:
        params = {
            "name": payload,
            "Submit": "Submit"
        }

        response = session.get(url, params=params)

        if payload.lower() in response.text.lower():
            print("Possible XSS vulnerability detected!")
            print("Payload:", payload)
            print("URL:", response.url)

            results.append({
                "vulnerability": "XSS",
                "payload": payload,
                "url": response.url
            })

    if not results:
        print("Scan Completed. No XSS detected.")

    with open("xss_results.json", "w") as file:
        json.dump(results, file, indent=4)


login_dvwa()
set_security_low()

target = "http://localhost/dvwa/vulnerabilities/xss_r/"
test_xss(target)