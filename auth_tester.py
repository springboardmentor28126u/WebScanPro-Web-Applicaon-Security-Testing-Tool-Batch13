import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "http://localhost/dvwa"
LOGIN_URL = BASE_URL + "/login.php"

session = requests.Session()


# ---------------------------------------
# GET LOGIN TOKEN
# ---------------------------------------
def get_login_token():
    page = session.get(LOGIN_URL)
    soup = BeautifulSoup(page.text, "html.parser")
    token = soup.find("input", {"name": "user_token"})["value"]
    return token


# ---------------------------------------
# CHECK LOGIN SUCCESS
# ---------------------------------------
def login_success(response):
    if "Logout" in response.text or "logout.php" in response.text:
        return True
    return False


# ---------------------------------------
# WEAK CREDENTIAL TEST
# ---------------------------------------
def weak_credential_test():

    print("\n==============================")
    print(" Weak Credential Testing ")
    print("==============================")

    credentials = [
        ("admin", "admin"),
        ("admin", "password"),
        ("admin", "123456"),
        ("user", "password")
    ]

    results = []

    for username, password in credentials:

        token = get_login_token()

        login_data = {
            "username": username,
            "password": password,
            "Login": "Login",
            "user_token": token
        }

        response = session.post(LOGIN_URL, data=login_data)

        print("\nURL:", LOGIN_URL)
        print("Testing Credential:", username, ":", password)
        print("Response Code:", response.status_code)

        if login_success(response):
            print("Result: Weak Credential Found")

            results.append({
                "url": LOGIN_URL,
                "username": username,
                "password": password,
                "response_code": response.status_code,
                "vulnerability": "Weak Credentials"
            })
        else:
            print("Result: Login Failed")

    return results


# ---------------------------------------
# BRUTE FORCE TEST
# ---------------------------------------
def brute_force_test():

    print("\n==============================")
    print(" Brute Force Testing ")
    print("==============================")

    passwords = ["123", "1234", "12345", "password", "admin"]

    results = []

    for password in passwords:

        token = get_login_token()

        login_data = {
            "username": "admin",
            "password": password,
            "Login": "Login",
            "user_token": token
        }

        response = session.post(LOGIN_URL, data=login_data)

        print("\nURL:", LOGIN_URL)
        print("Brute Force Password:", password)
        print("Response Code:", response.status_code)

        if login_success(response):
            print("Result: Password Found via Brute Force")

            results.append({
                "url": LOGIN_URL,
                "password": password,
                "response_code": response.status_code,
                "vulnerability": "Brute Force Attack"
            })
        else:
            print("Result: Failed Attempt")

    return results


# ---------------------------------------
# COOKIE SECURITY TEST
# ---------------------------------------
def cookie_security_test():

    print("\n==============================")
    print(" Cookie Security Testing ")
    print("==============================")

    token = get_login_token()

    login_data = {
        "username": "admin",
        "password": "password",
        "Login": "Login",
        "user_token": token
    }

    session.post(LOGIN_URL, data=login_data)

    cookies = session.cookies

    results = []

    for cookie in cookies:

        print("\nURL:", LOGIN_URL)
        print("Cookie Name:", cookie.name)
        print("Cookie Value:", cookie.value)
        print("Secure Flag:", cookie.secure)

        if not cookie.secure:
            print("Result: Insecure Cookie Detected")

            results.append({
                "url": LOGIN_URL,
                "cookie_name": cookie.name,
                "secure_flag": cookie.secure,
                "vulnerability": "Insecure Cookie"
            })
        else:
            print("Result: Secure Cookie")

    return results


# ---------------------------------------
# SESSION FIXATION TEST
# ---------------------------------------
def session_fixation_test():

    print("\n==============================")
    print(" Session Fixation Testing ")
    print("==============================")

    session_before = session.cookies.get("PHPSESSID")

    token = get_login_token()

    login_data = {
        "username": "admin",
        "password": "password",
        "Login": "Login",
        "user_token": token
    }

    session.post(LOGIN_URL, data=login_data)

    session_after = session.cookies.get("PHPSESSID")

    print("\nURL:", LOGIN_URL)
    print("Session Before Login:", session_before)
    print("Session After Login:", session_after)

    results = []

    if session_before == session_after:
        print("Result: Session Fixation Vulnerability Detected")

        results.append({
            "url": LOGIN_URL,
            "session_before": session_before,
            "session_after": session_after,
            "vulnerability": "Session Fixation"
        })
    else:
        print("Result: Session Changed (Secure)")

    return results


# ---------------------------------------
# RUN ALL AUTH TESTS
# ---------------------------------------
def run_auth_tests():

    weak = weak_credential_test()
    brute = brute_force_test()
    cookie = cookie_security_test()
    session_test = session_fixation_test()

    all_results = weak + brute + cookie + session_test

    if all_results:
        with open("auth_report.json", "w") as f:
            json.dump(all_results, f, indent=4)

        print("\nAuthentication Report Saved → auth_report.json")

    return all_results


# ---------------------------------------
# RUN FILE
# ---------------------------------------
if __name__ == "__main__":
    run_auth_tests()