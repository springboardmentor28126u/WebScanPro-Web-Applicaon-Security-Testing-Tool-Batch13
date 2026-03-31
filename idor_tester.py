import requests
from bs4 import BeautifulSoup
import json
import time

# ── Config ────────────────────────────────────────────────────────────────────

base_url  = "http://localhost:8080"
login_url = base_url + "/login.php"

findings = []  # stores all vulnerabilities found


# ── Helper: get CSRF token ────────────────────────────────────────────────────

def get_csrf_token(session, url):
    res   = session.get(url)
    soup  = BeautifulSoup(res.text, "html.parser")
    token = soup.find("input", {"name": "user_token"})
    if token:
        return token.get("value")
    return None


# ── Helper: login and return a logged-in session ──────────────────────────────

def login(username="admin", password="password"):
    session = requests.Session()
    token   = get_csrf_token(session, login_url)

    data = {
        "username":   username,
        "password":   password,
        "Login":      "Login",
        "user_token": token
    }

    session.post(login_url, data=data, allow_redirects=True)
    return session


# ══════════════════════════════════════════════════════════════════════════════
# TEST 1 -- Horizontal Privilege Escalation
# ══════════════════════════════════════════════════════════════════════════════

def test_horizontal_privilege_escalation():
    print("\n" + "=" * 60)
    print("TEST 1 -- Horizontal Privilege Escalation")
    print("=" * 60)
    print("  Checking if one user can access another user's data")
    print("  by simply changing the user ID in the URL...\n")

    # log in as admin
    session = login("admin", "password")

    # DVWA's user info page -- try different user IDs
    # horizontal escalation = same level user accessing another user's data
    user_ids = ["1", "2", "3", "4", "5"]

    accessible = []

    for user_id in user_ids:
        url  = base_url + f"/vulnerabilities/sqli/?id={user_id}&Submit=Submit"
        resp = session.get(url)

        # check if we got actual user data back
        if "First name" in resp.text and "Surname" in resp.text:
            print(f"  [VULNERABLE]  User ID {user_id} -- data returned without ownership check")
            accessible.append(user_id)
            findings.append({
                "test":           "Horizontal Privilege Escalation",
                "user_id":        user_id,
                "url":            url,
                "evidence":       f"Accessed user ID {user_id} data without verifying ownership -- any logged-in user can see any other user's data",
                "severity":       "High",
                "recommendation": "Always verify that the logged-in user owns the requested resource before returning data."
            })
        else:
            print(f"  [safe]        User ID {user_id} -- no data returned or access denied")

        time.sleep(0.3)

    print("\n" + "-" * 60)
    if not accessible:
        print("  No horizontal privilege escalation found.")
    else:
        print(f"  Found {len(accessible)} accessible user ID(s): {accessible}")


# ══════════════════════════════════════════════════════════════════════════════
# TEST 2 -- Vertical Privilege Escalation
# ══════════════════════════════════════════════════════════════════════════════

def test_vertical_privilege_escalation():
    print("\n" + "=" * 60)
    print("TEST 2 -- Vertical Privilege Escalation")
    print("=" * 60)
    print("  Checking if a normal user can access admin-only pages...\n")

    # log in as admin first (DVWA only has one user so we simulate
    # by checking if restricted pages are accessible without proper role)
    session = login("admin", "password")

    # these are admin/privileged pages that should be restricted
    restricted_pages = [
        "/security.php",
        "/setup.php",
        "/phpinfo.php",
        "/vulnerabilities/",
    ]

    for page in restricted_pages:
        url  = base_url + page
        resp = session.get(url)

        # if we get 200 and actual content -- accessible
        if resp.status_code == 200 and "404" not in resp.text and "denied" not in resp.text.lower():
            print(f"  [VULNERABLE]  {page} -- accessible without strict role check (status: {resp.status_code})")
            findings.append({
                "test":           "Vertical Privilege Escalation",
                "page":           page,
                "url":            url,
                "status_code":    resp.status_code,
                "evidence":       f"Page {page} returned HTTP 200 -- no strict admin role enforcement found",
                "severity":       "High",
                "recommendation": "Implement role-based access control (RBAC). Verify user role before serving restricted pages."
            })
        else:
            print(f"  [safe]        {page} -- access denied or not found (status: {resp.status_code})")

        time.sleep(0.3)

    print("\n" + "-" * 60)


# ══════════════════════════════════════════════════════════════════════════════
# TEST 3 -- IDOR (Insecure Direct Object Reference)
# ══════════════════════════════════════════════════════════════════════════════

def test_idor():
    print("\n" + "=" * 60)
    print("TEST 3 -- IDOR (Insecure Direct Object Reference)")
    print("=" * 60)
    print("  Modifying parameters in requests to access")
    print("  objects or data that shouldn't be accessible...\n")

    session = login("admin", "password")

    # IDOR test 1 -- try to access different user profiles by changing id param
    print("  [*] Testing user ID parameter manipulation on /sqli/ page...")
    idor_ids = ["1", "2", "3", "4", "5", "6", "7", "8"]
    idor_found = []

    for uid in idor_ids:
        url  = base_url + f"/vulnerabilities/sqli/?id={uid}&Submit=Submit"
        resp = session.get(url)

        if "First name" in resp.text:
            # extract name from response
            soup      = BeautifulSoup(resp.text, "html.parser")
            pre_tags  = soup.find_all("pre")
            user_data = " | ".join([p.text.strip() for p in pre_tags]) if pre_tags else "data found"

            print(f"  [VULNERABLE]  ID={uid}  -->  {user_data[:80]}")
            idor_found.append(uid)
            findings.append({
                "test":           "IDOR",
                "parameter":      "id",
                "value_tested":   uid,
                "url":            url,
                "evidence":       f"Changing id={uid} in URL returned another user's data without authorization check",
                "severity":       "High",
                "recommendation": "Never use direct object references in URLs. Use indirect references or validate ownership server-side."
            })
        else:
            print(f"  [safe]        ID={uid}  -- no data returned")

        time.sleep(0.3)

    # IDOR test 2 -- try changing security level parameter
    print("\n  [*] Testing security parameter manipulation on /security.php...")
    security_levels = ["low", "medium", "high", "impossible"]

    for level in security_levels:
        url  = base_url + "/security.php"
        data = {"security": level, "seclev_submit": "Submit"}
        resp = session.post(url, data=data)

        if resp.status_code == 200:
            print(f"  [VULNERABLE]  Security level changed to '{level}' via direct parameter -- no authorization check")
            findings.append({
                "test":           "IDOR",
                "parameter":      "security",
                "value_tested":   level,
                "url":            url,
                "evidence":       f"Security level changed to '{level}' by directly modifying the POST parameter",
                "severity":       "Medium",
                "recommendation": "Validate and authorize all parameter changes server-side. Don't trust client input."
            })
            break

    print("\n" + "-" * 60)
    if not idor_found:
        print("  No IDOR vulnerabilities found.")
    else:
        print(f"  Found IDOR on {len(idor_found)} user ID(s): {idor_found}")


# ══════════════════════════════════════════════════════════════════════════════
# Summary
# ══════════════════════════════════════════════════════════════════════════════

def print_summary():
    print("\n" + "=" * 60)
    print("SCAN SUMMARY")
    print("=" * 60)

    if not findings:
        print("  No access control vulnerabilities found.")
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

    print("\n  Access Control Best Practices:")
    print("    1. RBAC (Role Based Access Control) -- assign permissions based on role not user")
    print("    2. ABAC (Attribute Based Access Control) -- check attributes like department, location")
    print("    3. Never use direct object IDs in URLs -- use indirect references or tokens")
    print("    4. Always verify ownership server-side -- never trust the client")
    print("    5. Apply least privilege -- users should only access what they need")
    print("    6. Log all access control failures for monitoring")
    print("    7. Deny access by default -- whitelist what is allowed, block everything else")


# ══════════════════════════════════════════════════════════════════════════════
# Save findings to JSON (for Week 7 report)
# ══════════════════════════════════════════════════════════════════════════════

def save_findings():
    with open("idor_findings.json", "w") as f:
        json.dump(findings, f, indent=4)
    print("\n  Findings saved to idor_findings.json")


# ══════════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 60)
print("  WebScanPro -- Week 6: Access Control & IDOR Testing")
print("=" * 60)

test_horizontal_privilege_escalation()
test_vertical_privilege_escalation()
test_idor()
print_summary()
save_findings()