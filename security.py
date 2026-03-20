# week5_auth_testing.py — FIXED VERSION
# Run this first to debug your DVWA connection:
#   python week5_auth_testing.py

import requests
from bs4 import BeautifulSoup
import json
import time

# ─── CONFIG ────────────────────────────────────────────────────────────────────
BASE_URL  = "http://localhost:8080"
LOGIN_URL = f"{BASE_URL}/login.php"          # FIX 1: remove /dvwa/ prefix —
                                              # most Docker images serve DVWA
                                              # directly at / not /dvwa/
                                              # If yours uses /dvwa/, change back.

BRUTE_URL  = f"{BASE_URL}/vulnerabilities/brute/"
COOKIE_URL = f"{BASE_URL}/vulnerabilities/weak_id/"

USERNAMES = ["admin", "user", "root", "test", "gordonb", "pablo", "smithy"]
PASSWORDS = ["password", "123456", "admin", "letmein", "abc123",
             "charley", "dragon", "master", "monkey", "shadow"]

findings = []


# ─── STEP 0: DEBUG HELPER — run this first ─────────────────────────────────────
def debug_login():
    """
    BUG CAUSE: You never saw brute-force hits because the success
    detection string didn't match what DVWA actually returns.
    This function prints the real response so you can find the correct string.
    """
    session  = requests.Session()
    response = session.get(LOGIN_URL)
    soup     = BeautifulSoup(response.text, "html.parser")
    token    = soup.find("input", {"name": "user_token"})
    csrf     = token["value"] if token else ""

    # Try a known-good login
    resp = session.post(LOGIN_URL, data={
        "username":   "admin",
        "password":   "password",
        "Login":      "Login",
        "user_token": csrf
    })

    print("\n[DEBUG] Login response URL:", resp.url)
    print("[DEBUG] Status code:", resp.status_code)

    # Print all cookies so you can see the real cookie names
    print("[DEBUG] Cookies after login:")
    for name, value in session.cookies.items():
        print(f"        {name} = {value}")

    # Print a snippet of the response body to find the success string
    print("\n[DEBUG] Response body snippet (first 800 chars):")
    print(resp.text[:800])
    print("\n[DEBUG] ← Find a unique phrase above to use as success_marker")


# ─── HELPERS ───────────────────────────────────────────────────────────────────
def start_session(security="low"):
    """
    FIX 2: The original code used session.get() for the brute-force test.
    DVWA's brute force module at LOW security uses GET parameters — that part
    was correct. But the login itself must be a POST to /login.php.
    We also need to visit index.php after login to confirm the session is active.
    """
    session  = requests.Session()
    response = session.get(LOGIN_URL)
    soup     = BeautifulSoup(response.text, "html.parser")
    token    = soup.find("input", {"name": "user_token"})
    csrf     = token["value"] if token else ""

    login_resp = session.post(LOGIN_URL, data={
        "username":   "admin",
        "password":   "password",
        "Login":      "Login",
        "user_token": csrf
    })

    # Confirm login worked — should redirect to index.php
    if "index.php" in login_resp.url or "Welcome" in login_resp.text:
        print(f"[+] Login successful — session active")
    else:
        print(f"[!] WARNING — login may have failed. URL: {login_resp.url}")
        print("    Run debug_login() to inspect the response.")

    session.cookies.set("security", security)
    print(f"[+] Security level set to: {security}")
    return session


def get_csrf_token(session, url):
    response = session.get(url)
    soup     = BeautifulSoup(response.text, "html.parser")
    token    = soup.find("input", {"name": "user_token"})
    return token["value"] if token else ""


# ─── TEST 1: Brute Force ────────────────────────────────────────────────────────
def test_brute_force(session):
    """
    FIX 3: The original success string was:
        "Welcome to the password protected area"
    DVWA actually returns:
        "Welcome to the password protected area {username}"
    But more reliably, check for the ABSENCE of "Username and/or password incorrect"
    AND the presence of "Welcome" — because the exact phrasing varies by DVWA version.

    Also added: print the first 300 chars of each response while testing
    so you can see what's happening in real time.
    """
    print("\n[*] Running brute-force attack test...")
    found_any = False

    for username in USERNAMES:
        for password in PASSWORDS:
            token = get_csrf_token(session, BRUTE_URL)

            response = session.get(BRUTE_URL, params={
                "username":   username,
                "password":   password,
                "Login":      "Login",
                "user_token": token
            })

            body = response.text

            # FIX 3a: Use a more reliable success check
            # DVWA LOW shows "Welcome to the password protected area"
            # DVWA also never shows "incorrect" on a successful login
            login_success = (
                "Welcome to the password protected area" in body
                or ("Welcome" in body and "incorrect" not in body
                    and "password" not in body.lower()[:200])
            )

            login_blocked = (
                "CAPTCHA" in body
                or "Too many login" in body
                or "Account locked" in body
            )

            if login_success:
                found_any = True
                finding = {
                    "test":     "Brute Force",
                    "severity": "HIGH",
                    "detail":   f"Valid credentials found → {username} / {password}",
                    "fix":      "Add account lockout after 5 failed attempts; implement CAPTCHA"
                }
                findings.append(finding)
                print(f"    [!] VULNERABLE — login succeeded: {username} / {password}")

            elif login_blocked:
                print(f"    [+] PROTECTED — server blocked attempt for: {username}")
                break   # No point continuing if we're locked out

            else:
                print(f"    [-] Failed: {username} / {password}")

            time.sleep(0.15)

    if not found_any:
        print("\n    [NOTE] No credentials found — your DVWA may be on a path like")
        print("           /dvwa/vulnerabilities/brute/ instead of /vulnerabilities/brute/")
        print("           Run debug_login() to check, or try security level 'low' explicitly.")

    print("[*] Brute-force test complete.")


# ─── TEST 2: Default Credentials ───────────────────────────────────────────────
def test_default_credentials(session):
    """
    FIX 4: The original test sent POST requests to LOGIN_URL.
    The DVWA brute-force module uses GET requests to BRUTE_URL —
    not the main login page. We must send these to the brute force module,
    not the login form, because the login form has CSRF protection that
    makes replays harder.
    """
    print("\n[*] Testing default credentials via brute-force module...")

    pairs = [
        ("admin",   "admin"),
        ("admin",   "password"),    # This IS the real DVWA default
        ("root",    "root"),
        ("gordonb", "abc123"),      # DVWA's built-in test users
        ("pablo",   "letmein"),
        ("smithy",  "password"),
    ]

    for username, password in pairs:
        token    = get_csrf_token(session, BRUTE_URL)
        response = session.get(BRUTE_URL, params={
            "username":   username,
            "password":   password,
            "Login":      "Login",
            "user_token": token
        })

        if "Welcome to the password protected area" in response.text:
            finding = {
                "test":     "Default Credentials",
                "severity": "CRITICAL",
                "detail":   f"Default login accepted → {username} / {password}",
                "fix":      "Never ship with default credentials; force change on first login"
            }
            findings.append(finding)
            print(f"    [!] CRITICAL — accepted: {username} / {password}")
        elif "incorrect" in response.text.lower():
            print(f"    [+] Rejected: {username} / {password}")
        else:
            # Ambiguous — print snippet for debugging
            print(f"    [?] Unclear response for {username}/{password}:")
            print(f"        {response.text[200:400].strip()}")


# ─── TEST 3: Session Cookie Analysis ───────────────────────────────────────────
def test_session_cookies(session):
    """
    FIX 5: The original code looked for cookies named 'dvwaSession' on the
    response object. DVWA stores the weak session ID in a cookie, but you
    need to click the "Generate" button first, which is a GET with Submit=Generate.
    Also: print ALL cookies on every response so you can see the real names.
    """
    print("\n[*] Collecting session tokens from Weak Session IDs module...")

    session_ids = []

    for i in range(6):
        response = session.get(COOKIE_URL, params={"Submit": "Generate"})

        # Print all cookies to find the correct name
        if i == 0:
            print("    [DEBUG] All cookies present:")
            for name, value in session.cookies.items():
                print(f"            {name} = {value}")

        # Try common cookie names DVWA uses for this module
        dvwa_session = (
            response.cookies.get("dvwaSession")
            or session.cookies.get("dvwaSession")
            or response.cookies.get("PHPSESSID")
            or session.cookies.get("PHPSESSID")
        )

        # Grab whatever cookie changed — compare before/after
        all_resp_cookies = dict(response.cookies)
        if all_resp_cookies:
            # Take the first one that isn't the main PHPSESSID or security cookie
            for cname, cval in all_resp_cookies.items():
                if cname not in ("security", "PHPSESSID"):
                    dvwa_session = cval
                    break

        if dvwa_session:
            session_ids.append(str(dvwa_session))
            print(f"    Token #{i+1}: {dvwa_session}")
        else:
            print(f"    Token #{i+1}: (none detected — see debug cookies above)")

    # Predictability check
    if len(session_ids) >= 3:
        numeric_ids = [s for s in session_ids if s.isdigit()]
        if len(numeric_ids) == len(session_ids):
            nums  = [int(t) for t in session_ids]
            diffs = [nums[j+1] - nums[j] for j in range(len(nums)-1)]
            if all(d == 1 for d in diffs):
                finding = {
                    "test":     "Weak Session IDs",
                    "severity": "HIGH",
                    "detail":   f"Tokens are sequential integers: {session_ids}",
                    "fix":      "Use secrets.token_hex(32) or UUID4 for session token generation"
                }
                findings.append(finding)
                print("    [!] VULNERABLE — tokens are sequential integers (easily guessable)")
            else:
                print(f"    [!] Tokens are numeric but not strictly sequential: {session_ids}")
                finding = {
                    "test":     "Weak Session IDs",
                    "severity": "MEDIUM",
                    "detail":   f"Tokens appear numeric/predictable: {session_ids}",
                    "fix":      "Use cryptographically random session tokens"
                }
                findings.append(finding)
        else:
            print(f"    [+] Tokens appear non-numeric: {session_ids}")
    else:
        print("    [NOTE] Not enough tokens collected to assess predictability.")
        print("           Check that DVWA's Weak Session IDs module is accessible.")

    check_cookie_flags(session)


def check_cookie_flags(session):
    """Check HttpOnly, Secure, and SameSite flags on all session cookies."""
    print("\n[*] Checking cookie security flags...")
    response = session.get(BASE_URL + "/index.php")

    checked = False
    for cookie in session.cookies:
        checked = True
        issues  = []

        # requests stores HttpOnly as a nonstandard attr
        # We check the raw Set-Cookie header more reliably:
        raw_headers = response.headers.get("Set-Cookie", "")

        if "httponly" not in raw_headers.lower():
            issues.append("HttpOnly not confirmed in Set-Cookie header")
        if "secure" not in raw_headers.lower():
            issues.append("Secure flag missing (cookie sent over HTTP)")
        if "samesite" not in raw_headers.lower():
            issues.append("SameSite attribute missing")

        if issues:
            finding = {
                "test":     "Insecure Cookie Flags",
                "severity": "MEDIUM",
                "detail":   f"Cookie '{cookie.name}': {'; '.join(issues)}",
                "fix":      "Set HttpOnly, Secure, SameSite=Strict on all session cookies"
            }
            findings.append(finding)
            print(f"    [!] '{cookie.name}': {'; '.join(issues)}")
        else:
            print(f"    [+] '{cookie.name}': flags look OK")

    if not checked:
        print("    [NOTE] No cookies found on index.php — check BASE_URL is correct")


# ─── TEST 4: Session Fixation ──────────────────────────────────────────────────
def test_session_fixation(session):
    """
    FIX 6: The original code read PHPSESSID from session.cookies before
    and after re-login. The issue was that the session already had a valid
    PHPSESSID from start_session(), so the "before" value was never None —
    it was just not being read because of a path mismatch.

    Solution: start a FRESH unauthenticated session, record its PHPSESSID,
    then log in, then check if the PHPSESSID changed.
    """
    print("\n[*] Testing session fixation...")

    # Start completely fresh — no prior auth
    fresh = requests.Session()
    fresh.get(LOGIN_URL)   # Just visiting sets a PHPSESSID

    pre_login = fresh.cookies.get("PHPSESSID")
    print(f"    Token before login: {pre_login}")

    if not pre_login:
        print("    [NOTE] No PHPSESSID before login.")
        print("           DVWA may not issue a pre-login session cookie.")
        print("           This test requires the server to issue a cookie before auth.")
        return

    # Now authenticate with the fresh session
    response = fresh.get(LOGIN_URL)
    soup     = BeautifulSoup(response.text, "html.parser")
    token    = soup.find("input", {"name": "user_token"})
    csrf     = token["value"] if token else ""

    fresh.post(LOGIN_URL, data={
        "username":   "admin",
        "password":   "password",
        "Login":      "Login",
        "user_token": csrf
    })

    post_login = fresh.cookies.get("PHPSESSID")
    print(f"    Token after  login: {post_login}")

    if pre_login and post_login:
        if pre_login == post_login:
            finding = {
                "test":     "Session Fixation",
                "severity": "HIGH",
                "detail":   "PHPSESSID unchanged after login — fixation attack possible",
                "fix":      "Call session_regenerate_id(true) immediately after successful login"
            }
            findings.append(finding)
            print("    [!] VULNERABLE — session ID not regenerated after login")
        else:
            print("    [+] PROTECTED — session ID was regenerated after login")
    else:
        print("    [NOTE] Could not compare tokens — one or both were None")
        print("           DVWA may not use PHPSESSID in this Docker image version")


# ─── REPORT ────────────────────────────────────────────────────────────────────
def save_report():
    report = {
        "module":   "Week 5 — Authentication & Session Testing",
        "total":    len(findings),
        "findings": findings
    }
    with open("week5_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print(f"\n{'='*55}")
    print(f"  WEEK 5 REPORT — {len(findings)} finding(s)")
    print(f"  Saved to week5_report.json")
    print(f"{'='*55}")
    for item in findings:
        print(f"  [{item['severity']}] {item['test']}")
        print(f"           {item['detail']}")


# ─── MAIN ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("="*55)
    print("  WebScanPro — Week 5: Auth & Session Testing")
    print("="*55)

    # ── Uncomment the next line to debug your DVWA path first ──
    # debug_login()
    # import sys; sys.exit()
    # ───────────────────────────────────────────────────────────

    session = start_session(security="low")

    test_brute_force(session)
    test_default_credentials(session)
    test_session_cookies(session)
    test_session_fixation(session)

    save_report()