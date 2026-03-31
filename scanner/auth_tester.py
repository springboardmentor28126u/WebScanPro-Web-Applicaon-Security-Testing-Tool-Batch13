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
                "url": login_url,
                "username": username,
                "password": password,
                "severity": "Medium",
                "remediation": {
                    "password_policy": "Enforce strong password policies.",
                    "mfa": "Enable multi-factor authentication.",
                    "block_defaults": "Disable default credentials.",
                    "password_storage": "Store passwords securely using hashing."
                }
            })

    return findings   # ✅ THIS WAS MISSING
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
    "url": login_url,
    "password": password,
    "severity": "High",
    "remediation": {
        "rate_limit": "Implement rate limiting.",
        "account_lock": "Lock account after failed attempts.",
        "captcha": "Use CAPTCHA after multiple failures.",
        "monitoring": "Monitor login attempts and alert suspicious activity."
    }
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
    "url": url,
    "cookie": cookie.name,
    "issue": "Missing Secure flag",
    "severity": "Low",
    "remediation": {
        "secure_flag": "Set Secure flag on cookies.",
        "https": "Use HTTPS for all communications.",
        "cookie_scope": "Limit cookie scope and exposure."
    }
})

        if not cookie.has_nonstandard_attr('HttpOnly'):
            findings.append({
    "type": "Insecure Cookie",
    "cookie": cookie.name,
    "issue": "Missing HttpOnly flag",
    "severity": "Low",
    "remediation": {
        "httponly": "Set HttpOnly flag on cookies.",
        "xss_protection": "Prevent access via JavaScript.",
        "secure_cookies": "Use secure cookie attributes."
    }
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
    "url": login_url,
    "issue": "Session ID did not change after login",
    "severity": "Medium",
    "remediation": {
        "session_regen": "Regenerate session ID after login.",
        "invalidate_old": "Invalidate old session identifiers.",
        "secure_session": "Use secure session handling mechanisms."
    }
})

    return findings