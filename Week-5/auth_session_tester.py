import os
import requests
import json
from bs4 import BeautifulSoup

# ---------------- PATH SETUP ---------------- #

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CREDENTIAL_FILE = os.path.join(BASE_DIR, "credentials.txt")
RESULT_FILE = os.path.join(BASE_DIR, "auth_results.json")

login_url = "http://localhost/dvwa/login.php"
protected_url = "http://localhost/dvwa/index.php"

results = []

total_tested = 0
weak_found = 0


# ---------------- LOAD CREDENTIALS ---------------- #

def load_credentials():

    creds = []

    if not os.path.exists(CREDENTIAL_FILE):
        print("[!] credentials.txt not found.")
        return creds

    with open(CREDENTIAL_FILE, "r") as f:
        for line in f:
            if ":" in line:
                username, password = line.strip().split(":")
                creds.append((username, password))

    return creds


# ---------------- AI PASSWORD GENERATOR ---------------- #

def ai_generate_passwords():

    base_words = ["admin", "password", "root", "test"]

    numbers = ["123", "1234", "123456", "2024"]

    generated = []

    for word in base_words:
        for num in numbers:
            generated.append(word + num)

    return generated


# ---------------- LOGIN SUCCESS CHECK ---------------- #

def login_success(response_text):

    keywords = ["logout", "welcome", "dashboard"]

    for word in keywords:
        if word in response_text.lower():
            return True

    return False


# ---------------- GET CSRF TOKEN ---------------- #

def get_token(session):

    r = session.get(login_url)

    soup = BeautifulSoup(r.text, "html.parser")

    token_input = soup.find("input", {"name": "user_token"})

    if token_input:
        return token_input["value"]

    return None


# ---------------- LOGIN ATTEMPT ---------------- #

def attempt_login(username, password):

    global total_tested
    global weak_found

    total_tested += 1

    session = requests.Session()

    token = get_token(session)

    if not token:
        return None

    data = {
        "username": username,
        "password": password,
        "Login": "Login",
        "user_token": token
    }

    r = session.post(login_url, data=data)

    if login_success(r.text):

        weak_found += 1

        print(f"[VULNERABLE] Weak credential found: {username}:{password}")

        results.append({
            "type": "Weak Credentials",
            "username": username,
            "password": password,
            "severity": "High",
            "recommendation": "Use strong passwords and enforce password policy"
        })

        return session

    return None


# ---------------- CREDENTIAL TEST ---------------- #

def test_credentials():

    print("[*] Testing default credentials...")

    creds = load_credentials()

    valid_session = None

    for username, password in creds:

        session = attempt_login(username, password)

        if session and not valid_session:
            valid_session = session

    print("[*] Running AI password guessing...")

    ai_pwds = ai_generate_passwords()

    for pwd in ai_pwds:

        session = attempt_login("admin", pwd)

        if session and not valid_session:
            valid_session = session

    return valid_session


# ---------------- COOKIE CHECK ---------------- #

def check_cookies():

    print("[*] Checking cookies...")

    r = requests.get(login_url)

    for cookie in r.cookies:

        print("[+] Cookie detected:", cookie.name)

        results.append({
            "type": "Cookie Security",
            "cookie_name": cookie.name,
            "severity": "Medium",
            "recommendation": "Use Secure and HttpOnly cookie flags"
        })


# ---------------- SESSION FIXATION TEST ---------------- #

def test_session_fixation():

    print("[*] Testing session fixation...")

    session = requests.Session()

    session.get(login_url)

    before = session.cookies.get("PHPSESSID")

    token = get_token(session)

    data = {
        "username": "admin",
        "password": "password",
        "Login": "Login",
        "user_token": token
    }

    session.post(login_url, data=data)

    after = session.cookies.get("PHPSESSID")

    if before == after:

        print("[VULNERABLE] Session Fixation detected")

        results.append({
            "type": "Session Fixation",
            "severity": "High",
            "recommendation": "Regenerate session ID after login"
        })


# ---------------- SESSION HIJACK TEST ---------------- #

def test_session_hijacking(session):

    if not session:
        return

    print("[*] Testing session hijacking simulation...")

    cookies = session.cookies.get_dict()

    hijack = requests.get(protected_url, cookies=cookies)

    if "logout" in hijack.text.lower():

        print("[WARNING] Session cookie can access authenticated page")

        results.append({
            "type": "Session Hijacking Risk",
            "severity": "High",
            "recommendation": "Use HTTPS and secure cookies"
        })


# ---------------- SAVE RESULTS ---------------- #

def save_results():

    with open(RESULT_FILE, "w") as f:
        json.dump(results, f, indent=4)

    print("[+] Results saved to auth_results.json")


# ---------------- RUN MODULE ---------------- #

def run_auth_tests():

    print("\n===================================")
    print(" AI Authentication & Session Tester")
    print("===================================\n")

    session = test_credentials()

    check_cookies()

    test_session_fixation()

    test_session_hijacking(session)

    save_results()

    print("\n----------- Scan Summary -----------")

    print(f"Credentials tested: {total_tested}")
    print(f"Weak credentials found: {weak_found}")

    print("------------------------------------\n")


# ---------------- MAIN ---------------- #

if __name__ == "__main__":

    try:
        run_auth_tests()
    except Exception as e:
        print("[!] Authentication & Session Module failed.")
        print(e)