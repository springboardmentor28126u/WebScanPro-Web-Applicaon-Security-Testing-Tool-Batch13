import requests
from bs4 import BeautifulSoup
import json

print("Scanner started...")

session = requests.Session()

# -------------------------------
# Step 1: Login to DVWA
# -------------------------------
login_page = session.get("http://localhost/dvwa/login.php")
soup = BeautifulSoup(login_page.text, "html.parser")
user_token = soup.find("input", {"name": "user_token"})["value"]

login_data = {
    "username": "admin",
    "password": "password",
    "Login": "Login",
    "user_token": user_token
}

session.post("http://localhost/dvwa/login.php", data=login_data)

# -------------------------------
# Step 2: Set Security LOW
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

# -------------------------------
# Step 3: Extract Forms
# -------------------------------

target_urls = [
    "http://localhost/dvwa/login.php",
    "http://localhost/dvwa/vulnerabilities/sqli/",
    "http://localhost/dvwa/vulnerabilities/xss_r/",
    "http://localhost/dvwa/vulnerabilities/xss_s/"
]

scan_data = {}

for url in target_urls:
    print(f"Scanning: {url}")
    response = session.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    forms = soup.find_all("form")

    forms_list = []

    for form in forms:
        form_details = {
            "action": form.get("action"),
            "method": form.get("method", "get"),
            "inputs": [
                {
                    "type": inp.get("type"),
                    "name": inp.get("name")
                }
                for inp in form.find_all("input")
            ]
        }

        forms_list.append(form_details)

    scan_data[url] = forms_list

# Save JSON
with open("scan_results.json", "w") as f:
    json.dump(scan_data, f, indent=4)

print("Scanning Completed ✅")
print("Metadata saved successfully")