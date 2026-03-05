
import os
import requests
import json

# ---------------- PATH SETUP ---------------- #

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CREDENTIAL_FILE = os.path.join(BASE_DIR, "credentials.txt")
RESULT_FILE = os.path.join(BASE_DIR, "auth_results.json")

login_url = "http://localhost/dvwa/login.php"

results = []


# ---------------- LOAD CREDENTIALS ---------------- #

def load_credentials():

    creds = []

    if not os.path.exists(CREDENTIAL_FILE):
        print("[!] credentials.txt not found in Week-5 folder.")
        return creds

    with open(CREDENTIAL_FILE, "r") as f:
        for line in f:
            if ":" in line:
                username, password = line.strip().split(":")
                creds.append((username, password))

    return creds


# ---------------- DEFAULT CREDENTIAL TEST ---------------- #

def test_default_credentials():

    print("[*] Testing default credentials...")

    credentials = load_credentials()

    if not credentials:
        print("[!] No credentials loaded.")
        return

    for username, password in credentials:

        data = {
            "username": username,
            "password": password,
            "Login": "Login"
        }

        try:
            r = requests.post(login_url, data=data)

            if "Login failed" not in r.text:

                print(f"[VULNERABLE] Weak credential found: {username}:{password}")

                results.append({
                    "type": "Weak Credentials",
                    "username": username,
                    "password": password,
                    "severity": "High"
                })

        except Exception as e:
            print("Error:", e)


# ---------------- COOKIE SECURITY CHECK ---------------- #

def check_cookie_security():

    print("[*] Checking cookies...")

    try:
        r = requests.get(login_url)

        for cookie in r.cookies:

            print("[+] Cookie found:", cookie.name)

            results.append({
                "type": "Cookie Found",
                "cookie_name": cookie.name,
                "severity": "Info"
            })

    except Exception as e:
        print("Error checking cookies:", e)


# ---------------- SAVE RESULTS ---------------- #

def save_results():

    with open(RESULT_FILE, "w") as f:
        json.dump(results, f, indent=4)

    print("[+] Results saved to Week-5/auth_results.json")


# ---------------- RUN TESTS ---------------- #

def run_auth_tests():

    print("\n==============================")
    print(" Authentication & Session Test")
    print("==============================\n")

    test_default_credentials()
    check_cookie_security()
    save_results()


# ---------------- MAIN ---------------- #

if __name__ == "__main__":
    run_auth_tests()
