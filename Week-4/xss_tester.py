import requests
import json
import os
from bs4 import BeautifulSoup

from ai.feature_extractor import extract_xss_features
from ai.ai_xss_engine import predict

# ---------------- PATH CONFIG ---------------- #

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCANNER_OUTPUT = os.path.join(BASE_DIR, "..", "Week-2", "output.json")
RESULT_FILE = os.path.join(BASE_DIR, "xss_results.json")

BASE_URL = "http://localhost/dvwa/"
LOGIN_URL = BASE_URL + "login.php"

session = requests.Session()

XSS_PAYLOAD = "<script>alert(1)</script>"

# ---------------- LOGIN FUNCTION ---------------- #

def login_dvwa():
    print("[+] Logging into DVWA for XSS testing...")

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

    # Set security LOW
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

import time

# ---------------- XSS TESTING ---------------- #

def test_xss(forms):

    vulnerable = []

    print("\n[+] Starting Hybrid AI-Enhanced XSS Testing...\n")

    for form in forms:

        action = form["action"]
        method = form["method"]
        inputs = form["inputs"]

        # Only test XSS pages
        if "xss" not in action.lower():
            continue

        input_names = [inp.get("name") for inp in inputs if inp.get("name")]
        if not input_names:
            continue

        print("=" * 60)
        print(f"[*] Testing: {action}")

        try:
            # Get CSRF token
            page_response = session.get(action)
            soup = BeautifulSoup(page_response.text, "html.parser")

            token_input = soup.find("input", {"name": "user_token"})
            user_token = token_input["value"] if token_input else ""

            # -------- Normal Request -------- #

            start_normal = time.time()

            if method == "get":
                normal_response = session.get(
                    action,
                    params={
                        input_names[0]: "test",
                        "Submit": "Submit",
                        "user_token": user_token
                    }
                )
            else:
                normal_response = session.post(
                    action,
                    data={
                        input_names[0]: "test",
                        "Submit": "Submit",
                        "user_token": user_token
                    }
                )

            normal_time = time.time() - start_normal
            normal_text = normal_response.text.lower()

            # -------- Injected Request -------- #

            start_injected = time.time()

            if method == "get":
                injected_response = session.get(
                    action,
                    params={
                        input_names[0]: XSS_PAYLOAD,
                        "Submit": "Submit",
                        "user_token": user_token
                    }
                )
            else:
                injected_response = session.post(
                    action,
                    data={
                        input_names[0]: XSS_PAYLOAD,
                        "Submit": "Submit",
                        "user_token": user_token
                    }
                )

            injected_time = time.time() - start_injected
            injected_text = injected_response.text.lower()

            # -------- CLI OUTPUT -------- #

            length_diff = len(injected_text) - len(normal_text)
            payload_reflected = XSS_PAYLOAD.lower() in injected_text

            print(f"Normal Status Code   : {normal_response.status_code}")
            print(f"Injected Status Code : {injected_response.status_code}")
            print(f"Normal Response Time : {round(normal_time, 4)} sec")
            print(f"Injected Resp Time   : {round(injected_time, 4)} sec")
            print(f"Response Length Diff : {length_diff}")
            print(f"Payload Reflected    : {payload_reflected}")

            # ---------------- RULE-BASED DETECTION ---------------- #

            rule_based_detected = False

            if payload_reflected:
                rule_based_detected = True

            if "<script>" in injected_text and "alert(1)" in injected_text:
                rule_based_detected = True

            if "&lt;script&gt;" in injected_text:
                rule_based_detected = True

            # ---------------- AI DETECTION ---------------- #

            features = extract_xss_features(
                normal_text,
                injected_text,
                injected_response.status_code
            )

            prediction, probability = predict(features)

            # ---------------- FINAL DECISION ---------------- #

            if rule_based_detected or prediction == 1:

                if rule_based_detected:
                    confidence = 92.0
                else:
                    confidence = round(probability * 100, 2)

                print("\n[✔] XSS Detected!")
                print(f"Confidence Score     : {confidence}%")

                vulnerable.append({
                    "url": action,
                    "method": method.upper(),
                    "payload": XSS_PAYLOAD,
                    "type": "XSS",
                    "severity": "High",
                    "confidence": confidence
                })

            else:
                print("[–] No XSS Detected.")

        except Exception as e:
            print(f"[!] Error testing {action}: {e}")
            continue

    print("=" * 60)
    return vulnerable


# ---------------- MAIN ---------------- #

if __name__ == "__main__":

    login_dvwa()

    forms = load_forms()
    if forms is None:
        exit()

    results = test_xss(forms)

    with open(RESULT_FILE, "w") as rf:
        json.dump({"vulnerabilities": results}, rf, indent=4)

    print("\nHybrid AI XSS Testing Completed ✅")
    print(f"Total Vulnerabilities Found: {len(results)}")