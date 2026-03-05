from urllib.parse import urljoin

ERROR_PAYLOADS = [
    "'",
    "\"",
    "' -- "
]

BOOLEAN_PAYLOADS = [
    "' AND 1=1 -- ",
    "' AND 1=2 -- "
]

SQL_ERROR_KEYWORDS = [
    "you have an error in your sql syntax",
    "warning: mysql",
    "unclosed quotation mark",
    "sql error",
    "mysql_fetch",
]

def test_sqli(session, target_data):
    findings = []

    for page in target_data:
        url = page["url"]
        forms = page["forms"]

        for form in forms:
            action = urljoin(url, form["action"])
            method = form["method"].lower()
            inputs = form["inputs"]

            for input_field in inputs:
                name = input_field["name"]
                if not name:
                    continue

                # Prepare baseline request data
                base_data = {}
                for field in inputs:
                    if field["name"]:
                        base_data[field["name"]] = "1"

                try:
                    # ---- BASELINE RESPONSE ----
                    if method == "post":
                        normal_response = session.post(action, data=base_data)
                    else:
                        normal_response = session.get(action, params=base_data)

                    normal_length = len(normal_response.text)

                except:
                    continue

                # ============================
                # 1️⃣ ERROR-BASED DETECTION
                # ============================
                for payload in ERROR_PAYLOADS:
                    test_data = base_data.copy()
                    test_data[name] = payload

                    try:
                        if method == "post":
                            response = session.post(action, data=test_data)
                        else:
                            response = session.get(action, params=test_data)

                        response_text = response.text.lower()
                        injected_length = len(response.text)
                        length_difference = abs(injected_length - normal_length)

                        error_detected = any(
                            keyword in response_text for keyword in SQL_ERROR_KEYWORDS
                        )

                        if error_detected and length_difference > 20:
                            findings.append({
                                "type": "Error-Based SQLi",
                                "url": action,
                                "parameter": name,
                                "payload": payload,
                                "baseline_length": normal_length,
                                "injected_length": injected_length,
                                "length_difference": length_difference,
                                "remediation": {
                                    "primary_fix": "Use parameterized queries (prepared statements).",
                                    "avoid": "Avoid concatenating raw user input into SQL queries.",
                                    "input_validation": "Validate and sanitize all user inputs.",
                                    "db_principle": "Apply least-privilege access to database users.",
                                    "error_handling": "Disable detailed SQL error messages in production."
                                }
                            })
                            break

                    except:
                        continue

                # ============================
                # 2️⃣ BOOLEAN-BASED DETECTION
                # ============================
                try:
                    true_data = base_data.copy()
                    false_data = base_data.copy()

                    true_data[name] = BOOLEAN_PAYLOADS[0]
                    false_data[name] = BOOLEAN_PAYLOADS[1]

                    if method == "post":
                        true_response = session.post(action, data=true_data)
                        false_response = session.post(action, data=false_data)
                    else:
                        true_response = session.get(action, params=true_data)
                        false_response = session.get(action, params=false_data)

                    true_length = len(true_response.text)
                    false_length = len(false_response.text)
                    difference = abs(true_length - false_length)

                    if difference > 30:
                        findings.append({
                            "type": "Boolean-Based SQLi",
                            "url": action,
                            "parameter": name,
                            "true_payload": BOOLEAN_PAYLOADS[0],
                            "false_payload": BOOLEAN_PAYLOADS[1],
                            "true_length": true_length,
                            "false_length": false_length,
                            "difference": difference,
                            "remediation": {
                                "primary_fix": "Use prepared statements instead of dynamic SQL queries.",
                                "avoid": "Do not embed raw user input directly into SQL logic.",
                                "input_validation": "Implement strict input validation.",
                                "db_principle": "Restrict database permissions.",
                                "error_handling": "Suppress detailed SQL errors in production."
                            }
                        })

                except:
                    continue

    return findings