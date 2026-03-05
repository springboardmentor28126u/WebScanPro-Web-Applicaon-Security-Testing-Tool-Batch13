# scanner/xss_tester.py

from urllib.parse import urljoin

XSS_PAYLOADS = [
    "<script>alert(1337)</script>",
    "\"><script>alert(1337)</script>",
    "<img src=x onerror=alert(1337)>"
]


def test_xss(session, target_data):
    findings = []

    for page in target_data:
        url = page["url"]
        forms = page["forms"]

        for form in forms:
            action = form["action"]
            method = form["method"].lower()
            inputs = form["inputs"]

            for input_field in inputs:
                name = input_field["name"]
                if not name:
                    continue

                base_data = {}
                for field in inputs:
                    if field["name"]:
                        base_data[field["name"]] = "test"

                for payload in XSS_PAYLOADS:
                    test_data = base_data.copy()
                    test_data[name] = payload

                    try:
                        # Inject payload
                        if method == "post":
                            response = session.post(action, data=test_data)
                        else:
                            response = session.get(action, params=test_data)

                        response_text = response.text

                        # ==============================
                        # 1️⃣ Reflected XSS Detection
                        # ==============================
                        if payload in response_text:
                            findings.append({
                                "type": "Reflected XSS",
                                "url": action,
                                "parameter": name,
                                "payload": payload,
                                "severity": "High",
                                "remediation": {
                                    "primary_fix": "Escape user input before rendering in HTML.",
                                    "framework": "Enable template auto-escaping.",
                                    "csp": "Implement strict Content Security Policy.",
                                    "validation": "Apply strict input validation.",
                                    "dom": "Avoid using innerHTML with user input."
                                }
                            })
                            break

                        # ==============================
                        # 2️⃣ Stored XSS Detection
                        # ==============================
                        verify_response = session.get(url)

                        if payload in verify_response.text:
                            findings.append({
                                "type": "Stored XSS",
                                "url": url,
                                "parameter": name,
                                "payload": payload,
                                "severity": "Critical",
                                "remediation": {
                                    "primary_fix": "Sanitize input before storing in database.",
                                    "encoding": "Encode output when rendering stored content.",
                                    "csp": "Implement strict Content Security Policy."
                                }
                            })
                            break

                        # ==============================
                        # 3️⃣ Basic DOM Risk Detection
                        # ==============================
                        if "innerHTML" in response_text or "document.write" in response_text:
                            findings.append({
                                "type": "Potential DOM-Based XSS",
                                "url": action,
                                "parameter": name,
                                "severity": "Medium",
                                "note": "Page uses dynamic DOM manipulation. Manual review recommended."
                            })

                    except Exception:
                        continue

    return findings


def test_xss_url_params(session, target_data):
    findings = []

    for page in target_data:
        url = page["url"]

        for payload in XSS_PAYLOADS:
            test_url = f"{url}?xss_test={payload}"

            try:
                response = session.get(test_url)

                if payload in response.text:
                    findings.append({
                        "type": "Reflected XSS (URL Parameter)",
                        "url": test_url,
                        "parameter": "xss_test",
                        "payload": payload,
                        "severity": "Medium",
                        "remediation": {
                            "primary_fix": "Validate and encode URL parameters.",
                            "csp": "Implement Content Security Policy."
                        }
                    })

            except Exception:
                continue

    return findings