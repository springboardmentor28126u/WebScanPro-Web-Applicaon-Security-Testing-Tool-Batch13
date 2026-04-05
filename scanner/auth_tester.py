import requests

DEFAULT_CREDENTIALS = [
    ("admin", "admin"),
    ("admin", "password"),
    ("test", "test")
]

COMMON_PASSWORDS = [
    "1234",
    "password",
    "admin",
    "root"
]


def test_default_credentials(session, login_url):
    findings = []

    for username, password in DEFAULT_CREDENTIALS:

        data = {
            "username": username,
            "password": password,
            "Login": "Login"
        }

        response = session.post(login_url, data=data)

        if "Login failed" not in response.text:
            findings.append({
                "type": "Weak Credentials",
                "url": login_url,
                "username": username,
                "password": password,
                "evidence": "Login successful with default credentials",
                "severity": "Medium",
                "remediation": {
                    "password_policy": "Enforce strong password policies.",
                    "mfa": "Enable multi-factor authentication.",
                    "block_defaults": "Disable default credentials.",
                    "password_storage": "Store passwords securely using hashing."
                }
            })

    return findings


def test_bruteforce(session, login_url):
    findings = []

    for password in COMMON_PASSWORDS:

        data = {
            "username": "admin",
            "password": password,
            "Login": "Login"
        }

        response = session.post(login_url, data=data)

        if "Login failed" not in response.text:
            findings.append({
                "type": "Brute Force Success",
                "url": login_url,
                "password": password,
                "evidence": "Login succeeded without rate limiting",
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

    session.get(url)

    for cookie in session.cookies:

        # 🔍 Secure flag check
        if not cookie.secure:
            findings.append({
                "type": "Insecure Cookie",
                "url": url,
                "cookie": cookie.name,
                "issue": "Missing Secure flag",
                "evidence": f"Cookie '{cookie.name}' sent over HTTP",
                "severity": "Low",
                "remediation": {
                    "secure_flag": "Set Secure flag on cookies.",
                    "https": "Use HTTPS for all communications.",
                    "cookie_scope": "Limit cookie scope and exposure."
                }
            })

        # 🔍 HttpOnly check (safe fallback)
        if not getattr(cookie, "_rest", {}).get("HttpOnly", False):
            findings.append({
                "type": "Insecure Cookie",
                "url": url,
                "cookie": cookie.name,
                "issue": "Missing HttpOnly flag",
                "evidence": f"Cookie '{cookie.name}' accessible via JavaScript",
                "severity": "Low",
                "remediation": {
                    "httponly": "Set HttpOnly flag on cookies.",
                    "xss_protection": "Prevent access via JavaScript.",
                    "secure_cookies": "Use secure cookie attributes."
                }
            })

        # 🔍 SameSite check (NEW)
        if not getattr(cookie, "_rest", {}).get("SameSite"):
            findings.append({
                "type": "Insecure Cookie",
                "url": url,
                "cookie": cookie.name,
                "issue": "Missing SameSite attribute",
                "evidence": f"Cookie '{cookie.name}' vulnerable to CSRF",
                "severity": "Medium",
                "remediation": {
                    "samesite": "Set SameSite=Strict or Lax.",
                    "csrf": "Implement CSRF protection tokens.",
                    "secure_design": "Restrict cross-site cookie usage."
                }
            })

    return findings


def test_session_fixation(session, login_url):
    findings = []

    # session before login
    before = session.cookies.get_dict().copy()

    data = {
        "username": "admin",
        "password": "password",
        "Login": "Login"
    }

    session.post(login_url, data=data)

    # session after login
    after = session.cookies.get_dict().copy()

    # 🔥 stronger check
    if before == after or not any(k not in before or before[k] != after[k] for k in after):
        findings.append({
            "type": "Session Fixation",
            "url": login_url,
            "issue": "Session ID did not change after login",
            "evidence": f"Before: {before} | After: {after}",
            "severity": "Medium",
            "remediation": {
                "session_regen": "Regenerate session ID after login.",
                "invalidate_old": "Invalidate old session identifiers.",
                "secure_session": "Use secure session handling mechanisms."
            }
        })

    return findings