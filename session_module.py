import requests
from bs4 import BeautifulSoup

BASE_URL  = "http://localhost:8080/dvwa/"
LOGIN_URL = BASE_URL + "login.php"


# ── Internal helpers ───────────────────────────────────────────────────────

def _get_token(session):
    resp = session.get(LOGIN_URL, timeout=5)
    soup = BeautifulSoup(resp.text, "html.parser")
    tag  = soup.find("input", {"name": "user_token"})
    return tag["value"] if tag else ""


def _login(session, username="admin", password="password"):
    token = _get_token(session)
    session.post(LOGIN_URL, data={
        "username":   username,
        "password":   password,
        "Login":      "Login",
        "user_token": token,
    }, timeout=5, allow_redirects=True)


# ── helper: safely get PHPSESSID ───────────────────────────────────────────

def _get_phpsessid(session):
    for c in session.cookies:
        if c.name == "PHPSESSID":
            return c.value
    return ""


# ── Test 1: Cookie Flag Analysis ───────────────────────────────────────────

def _test_cookie_flags(session):
    """Check DVWA cookies for missing HttpOnly / Secure / SameSite flags."""

    results = []
    session.get(LOGIN_URL, timeout=5)

    for cookie in session.cookies:

        missing = []

        if not getattr(cookie, "has_nonstandard_attr", lambda x: False)("HttpOnly"):
            missing.append("HttpOnly")

        if not cookie.secure:
            missing.append("Secure")

        if not getattr(cookie, "_rest", {}).get("SameSite"):
            missing.append("SameSite")

        severity = "High"   if "HttpOnly" in missing else \
                   "Medium" if missing else "None"
        status   = f"Missing: {', '.join(missing)}" if missing else "Secure"

        print(f"[SESSION] Cookie '{cookie.name}' -> {status} (Severity: {severity})")
        results.append((cookie.name, status, severity, "Cookie Flag"))

    return results


# ── Test 2: Session Token Entropy ──────────────────────────────────────────

def _test_token_entropy(session):
    """Short PHPSESSID tokens are easier to brute-force."""

    token = _get_phpsessid(session)
    weak  = len(token) < 26

    status   = "Weak token (too short)" if weak else "Adequate length"
    severity = "Medium" if weak else "None"

    print(f"[SESSION] Token entropy -> {status} (len={len(token)})")
    return [("PHPSESSID", status, severity, "Token Entropy")]


# ── Test 3: Session Fixation ───────────────────────────────────────────────

def _test_session_fixation():
    """Token should change after login; same token = session fixation."""

    session = requests.Session()
    session.get(LOGIN_URL, timeout=5)
    pre  = _get_phpsessid(session)

    _login(session)
    post = _get_phpsessid(session)

    vulnerable = (pre == post and pre != "")
    status     = "Vulnerable — token not rotated on login" if vulnerable else "Safe — token rotated"
    severity   = "High" if vulnerable else "None"

    print(f"[SESSION] Session fixation -> {status}")
    return [("PHPSESSID", status, severity, "Session Fixation")]


# ── Test 4: Session Invalidation After Logout ──────────────────────────────

def _test_session_invalidation():
    """Old session cookie should stop working after logout."""

    session = requests.Session()
    _login(session)

    old_token = _get_phpsessid(session)
    old_cookie = {"PHPSESSID": old_token}

    session.get(BASE_URL + "logout.php", timeout=5)

    protected = BASE_URL + "vulnerabilities/sqli/"
    resp = requests.get(protected, cookies=old_cookie, timeout=5, allow_redirects=True)

    still_valid = "login.php" not in resp.url and resp.status_code == 200 and len(resp.text) > 300
    status      = "Vulnerable — session still valid after logout" if still_valid else "Safe — session invalidated"
    severity    = "High" if still_valid else "None"

    print(f"[SESSION] Session invalidation -> {status}")
    return [("Session Cookie", status, severity, "Session Invalidation")]


# ── Public runner ──────────────────────────────────────────────────────────

def run_session_scan(session):
    """
    Run all session/cookie tests.
    Returns a flat list of tuples: (name, status, severity, test_type)
    """
    print("\n🔎 Starting Session & Cookie Testing...\n")

    results = []
    results += _test_cookie_flags(session)
    results += _test_token_entropy(session)
    results += _test_session_fixation()
    results += _test_session_invalidation()

    vuln = sum(1 for _, _, sev, _ in results if sev != "None")
    print(f"\n[SESSION] Total findings: {vuln} / {len(results)}")
    return results