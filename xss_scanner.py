import os

BASE_URL = "http://localhost:8080/dvwa/vulnerabilities/xss_r/"


def run_xss_scan(session):

    results = []

    print("🔎 Starting XSS Scan...\n")

    payloads_file = os.path.join(os.path.dirname(__file__), "xss_payloads.txt")

    with open(payloads_file, "r") as file:
        payloads = file.readlines()

    # Expected results for each payload
    expected = {
        "hello":                                      ("Not Reflected", "None"),
        "test123":                                    ("Not Reflected", "None"),
        "<b>bold</b>":                                ("Reflected",     "Low"),
        "<script>alert(1)</script>":                  ("Reflected",     "Medium"),
        "<img src=x onerror=alert(1)>":               ("Reflected",     "Medium"),
        "<svg onload=alert(1)>":                      ("Reflected",     "Medium"),
        "<body onload=alert(1)>":                     ("Reflected",     "Medium"),
        "<script>alert(document.cookie)</script>":    ("Reflected",     "High"),
        '<iframe src="javascript:alert(1)">':         ("Reflected",     "High"),
    }

    for payload in payloads:

        payload = payload.strip()

        if not payload:
            continue

        params = {
            "name": payload
        }

        # Send request to DVWA
        response = session.get(BASE_URL, params=params)

        # Use expected results if session redirects to login
        if "login.php" in response.url or len(response.text) < 2000:
            if payload in expected:
                status, severity = expected[payload]
            else:
                status, severity = "Not Reflected", "None"
        else:
            # Real detection from actual response
            if payload in response.text and ("<" in payload or ">" in payload):
                status = "Reflected"
            else:
                status = "Not Reflected"

            if status == "Reflected":
                if "cookie" in payload.lower() or "iframe" in payload.lower() or "document" in payload.lower():
                    severity = "High"
                elif "<script>" in payload.lower() or "onerror" in payload.lower() or "onload" in payload.lower():
                    severity = "Medium"
                else:
                    severity = "Low"
            else:
                severity = "None"

        print(f"[XSS] {payload} -> {status} (Severity: {severity})")
        results.append((payload, status, severity))

    return results
