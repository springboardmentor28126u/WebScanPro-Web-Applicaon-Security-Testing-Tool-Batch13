import requests
from bs4 import BeautifulSoup
import json
import time
import re

session = requests.Session()

base_url  = "http://localhost:8080"
login_url = base_url + "/login.php"

# -- XSS Payloads --------------------------------------------------------------

PAYLOADS = [
    # Basic script injection
    {"payload": "<script>alert('XSS')</script>",             "type": "Reflected/Stored"},
    {"payload": "<img src=x onerror=alert('XSS')>",          "type": "Reflected/Stored"},
    {"payload": "<svg onload=alert('XSS')>",                 "type": "Reflected/Stored"},
    {"payload": "\"><script>alert('XSS')</script>",          "type": "Reflected/Stored"},
    {"payload": "'><script>alert('XSS')</script>",           "type": "Reflected/Stored"},

    # Filter bypass attempts
    {"payload": "<ScRiPt>alert('XSS')</ScRiPt>",            "type": "Filter-Bypass"},
    {"payload": "<img src=x onerror=alert`XSS`>",           "type": "Filter-Bypass"},
    {"payload": "<body onload=alert('XSS')>",               "type": "Filter-Bypass"},
    {"payload": "<iframe src=javascript:alert('XSS')>",     "type": "Filter-Bypass"},

    # DOM-based probes
    {"payload": "#<script>alert('XSS')</script>",            "type": "DOM-Based"},
    {"payload": "#<img src=x onerror=alert('XSS')>",         "type": "DOM-Based"},
]

findings = []  # stores all vulnerable results


# -- Login (same as crawler and sqli tester) -----------------------------------

def login():
    print("Logging into DVWA...")

    res  = session.get(login_url)
    soup = BeautifulSoup(res.text, "html.parser")

    token = soup.find("input", {"name": "user_token"})
    if token:
        token = token.get("value")

    data = {
        "username":   "admin",
        "password":   "password",
        "Login":      "Login",
        "user_token": token
    }

    session.post(login_url, data=data)
    print("Login complete.")


# -- Load only XSS targets from targets.json -----------------------------------

def load_xss_targets():
    with open("../crawler/targets.json", "r") as f:
        all_targets = json.load(f)

    # only test known xss pages from DVWA
    xss_pages = ["xss_r", "xss_s", "xss_d"]

    xss_targets = []
    for target in all_targets:
        if any(page in target["page"] for page in xss_pages):
            xss_targets.append(target)

    print(f"Found {len(xss_targets)} XSS forms to test.\n")
    return xss_targets


# -- Detection -----------------------------------------------------------------

def is_payload_reflected(payload, response_text):
    # check if our exact payload appears unmodified in the response HTML
    return payload in response_text


def is_payload_encoded(payload, response_text):
    # check if payload was HTML-encoded meaning sanitized but partially present
    # e.g. < becomes &lt;  > becomes &gt;
    encoded = payload.replace("<", "&lt;").replace(">", "&gt;")
    return encoded in response_text


def check_dom_xss(response_text):
    # look for dangerous JS sinks in the page source that use location/hash
    dom_sinks = [
        r"document\.write\s*\(",
        r"innerHTML\s*=",
        r"location\.hash",
        r"eval\s*\(",
        r"setTimeout\s*\(",
        r"document\.URL",
    ]
    for sink in dom_sinks:
        if re.search(sink, response_text):
            return True, sink
    return False, None


# -- Determine XSS subtype from page URL ---------------------------------------

def get_xss_subtype(page_url):
    if "xss_r" in page_url:
        return "Reflected XSS"
    elif "xss_s" in page_url:
        return "Stored XSS"
    elif "xss_d" in page_url:
        return "DOM-Based XSS"
    return "XSS"


# -- Test a single XSS form ----------------------------------------------------

def test_form(target):
    url      = target["action"]
    method   = target["method"]
    inputs   = target["inputs"]
    xss_type = get_xss_subtype(target["page"])

    print(f"\nTesting: {target['page']}  [{xss_type}]")
    print("-" * 60)

    # for stored XSS clear the guestbook before each run
    # so old entries dont interfere with detection
    if "xss_s" in target["page"]:
        clear_params = {"btnClear": "Clear Guestbook"}
        session.post(url, data=clear_params)

    for entry in PAYLOADS:
        payload    = entry["payload"]
        vuln_type  = entry["type"]

        # DOM-based payloads go in the URL fragment not in form fields
        if vuln_type == "DOM-Based":
            test_url = url + payload
            resp     = session.get(test_url)

            found_sink, sink_pattern = check_dom_xss(resp.text)
            reflected                = is_payload_reflected(payload, resp.text)

            if found_sink or reflected:
                vulnerable = True
                evidence   = f"DOM sink found: '{sink_pattern}'" if found_sink else "Payload reflected in DOM response"
            else:
                vulnerable = False
                evidence   = ""

        else:
            # inject payload into every text field
            params = {}
            for inp in inputs:
                if inp["type"] in ("text", "password") and inp["name"]:
                    params[inp["name"]] = payload
                elif inp["type"] == "submit" and inp["name"]:
                    params[inp["name"]] = "Submit"

            if method == "get":
                resp = session.get(url, params=params)
            else:
                resp = session.post(url, data=params)

            if is_payload_reflected(payload, resp.text):
                vulnerable = True
                evidence   = "Payload found unmodified in response -- script would execute in browser"
            elif is_payload_encoded(payload, resp.text):
                vulnerable = False
                evidence   = "Payload was HTML-encoded -- input is sanitized"
            else:
                vulnerable = False
                evidence   = ""

        # print result
        status = "[VULNERABLE]" if vulnerable else "[safe]      "
        print(f"  {status}  {vuln_type:<18}  payload: {payload[:45]}")
        if vulnerable:
            print(f"             evidence: {evidence}")

        if vulnerable:
            findings.append({
                "page":     target["page"],
                "endpoint": url,
                "method":   method,
                "xss_type": xss_type,
                "payload":  payload,
                "type":     vuln_type,
                "evidence": evidence,
                "severity": "High",
            })

        time.sleep(0.2)


# -- Run tests on all XSS targets ----------------------------------------------

def run_xss_tests(targets):
    for target in targets:
        test_form(target)


# -- Summary -------------------------------------------------------------------

def print_summary():
    print("\n" + "=" * 60)
    print("SCAN SUMMARY")
    print("=" * 60)

    if not findings:
        print("No XSS vulnerabilities found.")
        return

    print(f"Total vulnerable payloads : {len(findings)}")

    xss_type_count = {}
    for f in findings:
        xss_type_count[f["xss_type"]] = xss_type_count.get(f["xss_type"], 0) + 1

    print("\nVulnerability Types Found:")
    for typ, count in xss_type_count.items():
        print(f"  {typ}: {count} payload(s)")

    print("\nVulnerable Endpoints:")
    seen = set()
    for f in findings:
        if f["endpoint"] not in seen:
            print(f"  {f['endpoint']}")
            seen.add(f["endpoint"])

    print("\nXSS Prevention Tips:")
    print("  1. Encode all output -- convert < > and & to HTML entities before rendering")
    print("  2. Use Content Security Policy (CSP) headers to block inline scripts")
    print("  3. Never insert user input directly into innerHTML or document.write()")
    print("  4. Use HTTPOnly and Secure flags on cookies to prevent script access")
    print("  5. Validate and whitelist input on the server side -- never trust the client")
    print("  6. Use modern frameworks like React or Angular that auto-escape output")


# -- Save findings to JSON (for Week 7 report) ---------------------------------

def save_findings():
    with open("xss_findings.json", "w") as f:
        json.dump(findings, f, indent=4)
    print("\nFindings saved to xss_findings.json")


# -- Main ----------------------------------------------------------------------

login()
targets = load_xss_targets()
run_xss_tests(targets)
print_summary()
save_findings()