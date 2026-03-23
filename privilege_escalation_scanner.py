from bs4 import BeautifulSoup
import requests

BASE_URL      = "http://localhost:8080/dvwa/"
IDOR_ENDPOINT = BASE_URL + "vulnerabilities/sqli/"   # using SQLi page for IDOR-style testing
ADMIN_PAGES   = [
    "security.php",
    "phpinfo.php",
    "setup.php",
]

# ── Horizontal Privilege Escalation (IDOR) ───────────────────────────────

def test_horizontal_privilege_escalation(session):

    print("🔎 Testing Horizontal Privilege Escalation (IDOR)...\n")

    results = []
    test_ids = [1, 2, 3, 99, 999]

    for user_id in test_ids:

        params = {
            "id": user_id,
            "Submit": "Submit"
        }

        response = session.get(IDOR_ENDPOINT, params=params)

        # Detect user data in response
        if "First name:" in response.text and "Surname:" in response.text:
            status = "Accessible"

            # valid users
            if user_id in [1, 2, 3]:
                severity = "Medium"

            # unexpected access
            else:
                severity = "High"

        else:
            status = "Not Found"
            severity = "Low"

        print(f"[IDOR-H] id={user_id} -> {status} (Severity: {severity})")
        results.append((user_id, status, severity))

    return results


# ── Vertical Privilege Escalation ───────────────────────────────────────

def test_vertical_privilege_escalation(session):

    print("\n🔎 Testing Vertical Privilege Escalation...\n")

    results = []

    # login as low privilege user
    low_session = _get_low_priv_session()

    if low_session is None:
        print("[VERT] Could not log in as low-priv user")
        return results

    for page in ADMIN_PAGES:

        url = BASE_URL + page

        try:
            resp = low_session.get(url, timeout=5, allow_redirects=True)

            redirected_to_login = "login.php" in resp.url
            has_content = resp.status_code == 200 and len(resp.text) > 300

            if not redirected_to_login and has_content:
                status = "Accessible"
                severity = "High"
            else:
                status = "Blocked"
                severity = "None"

        except Exception as e:
            status = f"Error: {e}"
            severity = "None"

        print(f"[IDOR-V] /{page} -> {status} (Severity: {severity})")
        results.append((page, status, severity))

    return results


# ── Low Privilege Login ───────────────────────────────────────────────

def _get_low_priv_session():

    session   = requests.Session()
    login_url = BASE_URL + "login.php"

    try:
        resp  = session.get(login_url, timeout=5)
        soup  = BeautifulSoup(resp.text, "html.parser")

        token = soup.find("input", {"name": "user_token"})
        token = token["value"] if token else ""

        session.post(login_url, data={
            "username": "gordonb",
            "password": "abc123",
            "Login": "Login",
            "user_token": token,
        }, timeout=5)

        return session

    except Exception as e:
        print(f"[VERT] Login error: {e}")
        return None