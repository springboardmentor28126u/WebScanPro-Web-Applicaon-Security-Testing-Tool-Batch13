import requests

DEFAULT_CREDENTIALS = [
    ("admin", "admin"),
    ("admin", "password"),
    ("test", "test")
]

def test_default_credentials(login_url):
    findings = []

    for username, password in DEFAULT_CREDENTIALS:

        data = {
            "username": username,
            "password": password,
            "Login": "Login"
        }

        response = requests.post(login_url, data=data)

        if "Login failed" not in response.text:
            findings.append({
                "type": "Weak Credentials",
                "username": username,
                "password": password
            })

    return findings
COMMON_PASSWORDS = [
    "1234",
    "password",
    "admin",
    "root"
]

def test_bruteforce(login_url):

    findings = []

    for password in COMMON_PASSWORDS:

        data = {
            "username": "admin",
            "password": password,
            "Login": "Login"
        }

        response = requests.post(login_url, data=data)

        if "Login failed" not in response.text:
            findings.append({
                "type": "Brute Force Success",
                "password": password
            })

    return findings
def test_session_security(session, url):

    findings = []

    response = session.get(url)

    for cookie in session.cookies:

        print(cookie.name, cookie.secure)   # debug output you saw

        if not cookie.secure:
            findings.append({
                "type": "Insecure Cookie",
                "cookie": cookie.name,
                "issue": "Missing Secure flag"
            })

        if not cookie.has_nonstandard_attr('HttpOnly'):
            findings.append({
                "type": "Insecure Cookie",
                "cookie": cookie.name,
                "issue": "Missing HttpOnly flag"
            })

    return findings


def test_session_fixation(session, login_url):

    findings = []

    # session before login
    before = session.cookies.get_dict()

    # perform login again
    data = {
        "username": "admin",
        "password": "password",
        "Login": "Login"
    }

    session.post(login_url, data=data)

    # session after login
    after = session.cookies.get_dict()

    if before == after:
        findings.append({
            "type": "Session Fixation",
            "issue": "Session ID did not change after login"
        })

    return findings