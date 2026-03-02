import requests
import json
import os
import time
from bs4 import BeautifulSoup

from ai.feature_extractor import extract_features
from ai.ai_engine import predict

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

    print("\n[+] Starting Hybrid AI-Enhanced SQL Injection Testing...\n")

    for form in forms:

        action = form["action"]
        method = form["method"]
        inputs = form["inputs"]

        if "sqli" not in action.lower():
            continue

        input_names = [inp.get("name") for inp in inputs if inp.get("name")]
        if "id" not in input_names:
            continue

        print(f"[*] Testing {action}")

        try:

             # -------- Get CSRF token -------- #
            page_response = session.get(action)
            soup = BeautifulSoup(page_response.text, "html.parser")

            token_input = soup.find("input", {"name": "user_token"})
            user_token = token_input["value"] if token_input else ""

             # -------- Normal Request -------- #
            start_normal = time.time()
            normal_response = session.get(
                action,
                params={
                    "id": "1",
                    "Submit": "Submit",
                    "user_token": user_token
                }
            )
            normal_time = time.time() - start_normal
            normal_text = normal_response.text.lower()

            # -------- Injected Request -------- #
            payload = "' OR 1=1 --"

            start_injected = time.time()
            injected_response = session.get(
                action,
                params={
                    "id": payload,
                    "Submit": "Submit",
                    "user_token": user_token
                }
            )
            injected_time = time.time() - start_injected
            injected_text = injected_response.text.lower()
            
            # -------- CLI OUTPUT -------- #

            length_diff = len(injected_text) - len(normal_text)

            print(f"Normal Status Code   : {normal_response.status_code}")
            print(f"Injected Status Code : {injected_response.status_code}")
            print(f"Normal Response Time : {round(normal_time, 4)} sec")
            print(f"Injectth Died Resp Time   : {round(injected_time, 4)} sec")
            print(f"Response Lengff : {length_diff}")


            # ---------------- RULE-BASED DETECTION ---------------- #

            sql_error_patterns = [
                "you have an error in your sql syntax",
                "mysqli",
                "mysql",
                "warning",
                "fatal error"
            ]

            rule_based_detected = False

            for error in sql_error_patterns:
                if error in injected_text:
                    rule_based_detected = True
                    break

            if len(injected_text) > len(normal_text) + 100:
                rule_based_detected = True

            # ---------------- AI DETECTION ---------------- #

            features = extract_features(
                normal_text,
                injected_text,
                injected_response.status_code,
                normal_time,
                injected_time
            )

            prediction, probability = predict(features)

            # ---------------- FINAL DECISION ---------------- #

            if rule_based_detected or prediction == 1:

                if rule_based_detected:
                  confidence = 95.0   
                else:
                  confidence = round(probability * 100, 2)

                print(f"[✔] SQL Injection Detected at {action}")
                print(f"Confidence: {confidence}%\n")

                vulnerable.append({
                    "url": action,
                    "method": method.upper(),
                    "payload": payload,
                    "type": "SQL Injection",
                    "severity": "High",
                    "confidence": confidence
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

    print("\nHybrid AI SQLi Testing Completed ✅")
    print(f"Total Vulnerabilities Found: {len(results)}")