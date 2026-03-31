import requests
from bs4 import BeautifulSoup
import json
import time

# ── Config ────────────────────────────────────────────────────────────────────

base_url  = "http://localhost:8080"
login_url = base_url + "/login.php"

findings = []  # stores all vulnerabilities found


# ── Common weak credentials to try ───────────────────────────────────────────

WEAK_CREDENTIALS = [
    ("admin",  "admin"),
    ("admin",  "password"),
    ("admin",  "123456"),
    ("admin",  "password123"),
    ("admin",  "admin123"),
    ("admin",  "letmein"),
    ("admin",  "qwerty"),
    ("admin",  "welcome"),
    ("user",   "user"),
    ("user",   "password"),
    ("test",   "test"),
    ("root",   "root"),
    ("root",   "toor"),
    ("guest",  "guest"),
]

# ── Brute force password wordlist ─────────────────────────────────────────────

BRUTE_FORCE_PASSWORDS = [
    "123456", "12345678", "qwerty", "abc123", "monkey",
    "1234567", "letmein", "trustno1", "dragon", "baseball",
    "iloveyou", "master", "sunshine", "ashley", "bailey",
    "passw0rd", "shadow", "123123", "654321", "superman",
    "michael", "football", "password1", "welcome", "password",
]


# ── Helper: get CSRF token from login page ────────────────────────────────────

def get_csrf_token(session, url):
    res   = session.get(url)
    soup  = BeautifulSoup(res.text, "html.parser")
    token = soup.find("input", {"name": "user_token"})
    if token:
        return token.get("value")
    return None


# ── Helper: check if login was successful ─────────────────────────────────────

def is_logged_in(response_text):
    # failed login keeps you on login page with "Login failed" message
    # successful login redirects to index.php
    return "Login failed" not in response_text and "login.php" not in response_text


# ══════════════════════════════════════════════════════════════════════════════
# TEST 1 -- Weak / Default Credentials
# ══════════════════════════════════════════════════════════════════════════════

def test_weak_credentials():
    print("\n" + "=" * 60)
    print("TEST 1 -- Weak / Default Credentials")
    print("=" * 60)
    print("  Trying common username / password combinations...\n")

    vulnerable_creds = []

    for username, password in WEAK_CREDENTIALS:

        # use a fresh session for every attempt
        # so previous failed logins don't interfere
        session = requests.Session()
        token   = get_csrf_token(session, login_url)

        data = {
            "username":   username,
            "password":   password,
            "Login":      "Login",
            "user_token": token       # DVWA requires this or login is rejected
        }

        resp = session.post(login_url, data=data, allow_redirects=True)

        if is_logged_in(resp.text):
            print(f"  [VULNERABLE]  Login succeeded --  {username} / {password}")
            vulnerable_creds.append((username, password))

            findings.append({
                "test":           "Weak Credentials",
                "username":       username,
                "password":       password,
                "evidence":       f"Login succeeded with {username} / {password}",
                "severity":       "Critical",
                "recommendation": "Change all default credentials immediately. Enforce a strong password policy."
            })

        else:
            print(f"  [safe]        {username} / {password}")

        time.sleep(0.3)   # small delay between attempts

    # final result
    print("\n" + "-" * 60)
    if not vulnerable_creds:
        print("  No weak credentials found.")
    else:
        print(f"  Found {len(vulnerable_creds)} vulnerable credential(s):")
        for u, p in vulnerable_creds:
            print(f"    --> {u} / {p}")


# ══════════════════════════════════════════════════════════════════════════════
# TEST 2 -- Brute Force Attack
# ══════════════════════════════════════════════════════════════════════════════

def test_brute_force():
    print("\n" + "=" * 60)
    print("TEST 2 -- Brute Force Attack")
    print("=" * 60)
    print("  Rapidly trying passwords for username: admin")
    print("  Checking if site blocks or rate-limits attempts...\n")

    attempt_count = 0
    blocked       = False
    cracked_pass  = None

    for password in BRUTE_FORCE_PASSWORDS:
        session = requests.Session()
        token   = get_csrf_token(session, login_url)

        data = {
            "username":   "admin",
            "password":   password,
            "Login":      "Login",
            "user_token": token
        }

        start   = time.time()
        resp    = session.post(login_url, data=data, allow_redirects=True)
        elapsed = round(time.time() - start, 2)

        attempt_count += 1

        # check if site blocked us -- 429 = too many requests
        if resp.status_code == 429 or "locked" in resp.text.lower() or "too many" in resp.text.lower():
            print(f"  [PROTECTED]   Site blocked us after {attempt_count} attempts -- rate limiting works!")
            blocked = True
            findings.append({
                "test":           "Brute Force",
                "attempts":       attempt_count,
                "evidence":       f"Site blocked login after {attempt_count} attempts",
                "severity":       "Info",
                "recommendation": "Good -- rate limiting is in place. Keep it."
            })
            break

        # check if password was cracked
        if is_logged_in(resp.text):
            print(f"  [VULNERABLE]  Password cracked! -- admin / {password}  (attempt {attempt_count})")
            cracked_pass = password
            findings.append({
                "test":           "Brute Force",
                "username":       "admin",
                "password":       password,
                "attempts":       attempt_count,
                "evidence":       f"Password cracked after {attempt_count} attempts -- site never blocked the requests",
                "severity":       "Critical",
                "recommendation": "Add rate limiting. Lock account after 5 failed attempts. Add CAPTCHA."
            })
            break
        else:
            print(f"  [attempt {attempt_count:02}]  admin / {password:<20}  failed  ({elapsed}s)")

        time.sleep(0.3)

    # if we went through all passwords and were never blocked
    if not blocked and not cracked_pass:
        print(f"\n  [VULNERABLE]  Site never blocked us after {attempt_count} attempts -- no rate limiting!")
        findings.append({
            "test":           "Brute Force",
            "attempts":       attempt_count,
            "evidence":       f"Site allowed {attempt_count} login attempts with no blocking -- no rate limiting",
            "severity":       "High",
            "recommendation": "Add rate limiting. Lock account after 5 failed attempts. Add CAPTCHA."
        })

    print("\n" + "-" * 60)


# ══════════════════════════════════════════════════════════════════════════════
# TEST 3 -- Insecure Cookies
# ══════════════════════════════════════════════════════════════════════════════

def test_insecure_cookies():
    print("\n" + "=" * 60)
    print("TEST 3 -- Insecure Cookies")
    print("=" * 60)
    print("  Logging in and inspecting session cookies...\n")

    session = requests.Session()
    token   = get_csrf_token(session, login_url)

    data = {
        "username":   "admin",
        "password":   "password",
        "Login":      "Login",
        "user_token": token
    }

    session.post(login_url, data=data, allow_redirects=True)

    cookie_issues = []

    for cookie in session.cookies:
        print(f"  Cookie   : {cookie.name} = {cookie.value[:40]}...")
        print(f"  Secure   : {cookie.secure}")

        http_only = 'HttpOnly' in cookie._rest
        print(f"  HttpOnly : {http_only}")

        samesite  = cookie._rest.get('SameSite', 'Not Set')
        print(f"  SameSite : {samesite}")
        print()

        # check HttpOnly flag
        if not http_only:
            issue = f"Cookie '{cookie.name}' missing HttpOnly -- JavaScript can read and steal it via XSS"
            print(f"  [VULNERABLE]  {issue}")
            cookie_issues.append(issue)
            findings.append({
                "test":           "Insecure Cookie",
                "cookie":         cookie.name,
                "issue":          "Missing HttpOnly flag",
                "evidence":       issue,
                "severity":       "High",
                "recommendation": "Set HttpOnly flag on all session cookies to block JavaScript access."
            })

        # check Secure flag
        if not cookie.secure:
            issue = f"Cookie '{cookie.name}' missing Secure flag -- can be sent over plain HTTP and intercepted"
            print(f"  [VULNERABLE]  {issue}")
            cookie_issues.append(issue)
            findings.append({
                "test":           "Insecure Cookie",
                "cookie":         cookie.name,
                "issue":          "Missing Secure flag",
                "evidence":       issue,
                "severity":       "High",
                "recommendation": "Set Secure flag on all session cookies and enforce HTTPS."
            })

        # check SameSite attribute
        if samesite == "Not Set":
            issue = f"Cookie '{cookie.name}' missing SameSite attribute -- vulnerable to CSRF attacks"
            print(f"  [VULNERABLE]  {issue}")
            cookie_issues.append(issue)
            findings.append({
                "test":           "Insecure Cookie",
                "cookie":         cookie.name,
                "issue":          "Missing SameSite attribute",
                "evidence":       issue,
                "severity":       "Medium",
                "recommendation": "Set SameSite=Strict or SameSite=Lax on all session cookies."
            })

    print("\n" + "-" * 60)
    if not cookie_issues:
        print("  All cookies are properly secured.")
    else:
        print(f"  Found {len(cookie_issues)} cookie issue(s)!")


# ══════════════════════════════════════════════════════════════════════════════
# TEST 4 -- Session Fixation
# ══════════════════════════════════════════════════════════════════════════════

def test_session_fixation():
    print("\n" + "=" * 60)
    print("TEST 4 -- Session Fixation")
    print("=" * 60)
    print("  Checking if session ID changes after login...\n")

    session = requests.Session()

    # step 1 -- visit login page and record session ID before login
    session.get(login_url)
    session_before = session.cookies.get("PHPSESSID")
    print(f"  Session ID BEFORE login : {session_before}")

    # step 2 -- log in
    token = get_csrf_token(session, login_url)
    data  = {
        "username":   "admin",
        "password":   "password",
        "Login":      "Login",
        "user_token": token
    }
    session.post(login_url, data=data, allow_redirects=True)

    # step 3 -- record session ID after login
    session_after = session.cookies.get("PHPSESSID")
    print(f"  Session ID AFTER  login : {session_after}")

    # step 4 -- compare the two
    print("\n" + "-" * 60)
    if session_before and session_after and session_before == session_after:
        print(f"  [VULNERABLE]  Session ID did NOT change after login!")
        print(f"               An attacker can set a known session ID before login and hijack it after.")
        findings.append({
            "test":           "Session Fixation",
            "session_before": session_before,
            "session_after":  session_after,
            "evidence":       "Session ID is identical before and after login -- session fixation possible",
            "severity":       "High",
            "recommendation": "Regenerate a brand new session ID immediately after every successful login."
        })
    elif session_before != session_after:
        print(f"  [safe]  Session ID changed after login -- protected against session fixation.")
    else:
        print(f"  [INFO]  Could not retrieve session ID to compare.")


# ══════════════════════════════════════════════════════════════════════════════
# TEST 5 -- Session Hijacking
# ══════════════════════════════════════════════════════════════════════════════

def test_session_hijacking():
    print("\n" + "=" * 60)
    print("TEST 5 -- Session Hijacking")
    print("=" * 60)
    print("  Stealing admin session cookie and using it in a fresh session...\n")

    # step 1 -- log in as admin and grab the session cookie
    victim_session = requests.Session()
    token          = get_csrf_token(victim_session, login_url)

    data = {
        "username":   "admin",
        "password":   "password",
        "Login":      "Login",
        "user_token": token
    }

    victim_session.post(login_url, data=data, allow_redirects=True)
    stolen_cookie = victim_session.cookies.get("PHPSESSID")

    print(f"  Step 1 -- Logged in as admin")
    print(f"  Stolen cookie (PHPSESSID) : {stolen_cookie}")

    # step 2 -- open a completely fresh session -- attacker never logged in
    attacker_session = requests.Session()

    # step 3 -- inject the stolen cookie into the attacker session
    attacker_session.cookies.set("PHPSESSID", stolen_cookie)
    print(f"\n  Step 2 -- Injected stolen cookie into a brand new session (no login)")

    # step 4 -- try to access a protected page without logging in
    resp = attacker_session.get(base_url + "/index.php")

    # step 5 -- check if access was granted
    print("\n" + "-" * 60)
    if "Login" not in resp.text and "login.php" not in resp.text:
        print(f"  [VULNERABLE]  Session hijacking SUCCESSFUL!")
        print(f"               Accessed protected page using only the stolen cookie -- no password needed.")
        findings.append({
            "test":           "Session Hijacking",
            "stolen_cookie":  stolen_cookie,
            "evidence":       "Attacker accessed a protected page using only a stolen PHPSESSID -- no login required",
            "severity":       "Critical",
            "recommendation": "Use HTTPS to prevent cookie theft. Set short session timeouts. Regenerate session on login."
        })
    else:
        print(f"  [safe]  Session hijacking failed -- server rejected the stolen cookie.")


# ══════════════════════════════════════════════════════════════════════════════
# Summary
# ══════════════════════════════════════════════════════════════════════════════

def print_summary():
    print("\n" + "=" * 60)
    print("SCAN SUMMARY")
    print("=" * 60)

    if not findings:
        print("  No vulnerabilities found.")
        return

    print(f"  Total issues found : {len(findings)}\n")

    # count by severity
    severity_count = {}
    for f in findings:
        severity_count[f["severity"]] = severity_count.get(f["severity"], 0) + 1

    print("  Severity Breakdown:")
    for sev, count in severity_count.items():
        print(f"    {sev}: {count}")

    print("\n  All Issues Found:")
    for i, f in enumerate(findings, 1):
        print(f"\n  [{i}] Test     : {f['test']}")
        print(f"      Evidence : {f['evidence']}")
        print(f"      Severity : {f['severity']}")
        print(f"      Fix      : {f['recommendation']}")

    print("\n  Security Best Practices:")
    print("    1. Never use default credentials -- change them after setup")
    print("    2. Enforce strong passwords -- min 8 chars, letters + numbers + symbols")
    print("    3. Lock account after 5 failed login attempts")
    print("    4. Add CAPTCHA to prevent automated brute force")
    print("    5. Set HttpOnly flag on cookies -- stops JavaScript from stealing them")
    print("    6. Set Secure flag on cookies -- only sent over HTTPS")
    print("    7. Set SameSite=Strict on cookies -- prevents CSRF attacks")
    print("    8. Regenerate session ID after every login -- prevents session fixation")
    print("    9. Use HTTPS everywhere -- encrypts all traffic including cookies")
    print("   10. Set short session timeouts -- expire idle sessions automatically")


# ══════════════════════════════════════════════════════════════════════════════
# Save findings to JSON (for Week 7 report)
# ══════════════════════════════════════════════════════════════════════════════

def save_findings():
    with open("auth_findings.json", "w") as f:
        json.dump(findings, f, indent=4)
    print("\n  Findings saved to auth_findings.json")


# ══════════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 60)
print("  WebScanPro -- Week 5: Authentication & Session Testing")
print("=" * 60)

test_weak_credentials()
test_brute_force()
test_insecure_cookies()
test_session_fixation()
test_session_hijacking()
print_summary()
save_findings()
