import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


TEST_IDS = ["1", "2", "3", "4", "5", "10", "100"]


def modify_parameter(url, param, new_value):
    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    params[param] = new_value

    new_query = urlencode(params, doseq=True)

    return urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment
    ))


def test_idor(session, urls):
    findings = []

    for url in urls:

        parsed = urlparse(url)
        params = parse_qs(parsed.query)

        if not params:
            continue

        try:
            # 🔥 BASELINE RESPONSE
            original_response = session.get(url)
            original_length = len(original_response.text)
        except:
            continue

        for param in params:

            if "id" in param.lower():

                for test_id in TEST_IDS:

                    modified_url = modify_parameter(url, param, test_id)

                    try:
                        response = session.get(modified_url)
                        modified_length = len(response.text)

                        # 🔥 REAL DETECTION LOGIC
                        if response.status_code == 200 and abs(modified_length - original_length) > 30:

                            findings.append({
                                "type": "Potential IDOR",
                                "url": url,
                                "parameter": param,
                                "tested_value": test_id,
                                "original_length": original_length,
                                "modified_length": modified_length,
                                "difference": abs(modified_length - original_length),
                                "evidence": "Response size changed after modifying object ID",
                                "severity": "High",
                                "remediation": {
                                    "primary_fix": "Validate user authorization before returning object data.",
                                    "rbac": "Implement Role-Based Access Control (RBAC).",
                                    "abac": "Use Attribute-Based Access Control (ABAC).",
                                    "direct_reference": "Avoid exposing direct object identifiers.",
                                    "server_validation": "Verify ownership of objects server-side."
                                }
                            })

                    except requests.RequestException:
                        continue

    return findings


def test_horizontal_privilege_escalation(session, urls):
    findings = []

    for url in urls:

        if "user" in url or "account" in url:

            try:
                baseline = session.get(url)
                baseline_len = len(baseline.text)
            except:
                continue

            for test_id in TEST_IDS:

                modified_url = f"{url}?user_id={test_id}"

                try:
                    response = session.get(modified_url)
                    new_len = len(response.text)

                    if response.status_code == 200 and abs(new_len - baseline_len) > 30:

                        findings.append({
                            "type": "Horizontal Privilege Escalation",
                            "url": modified_url,
                            "tested_user_id": test_id,
                            "difference": abs(new_len - baseline_len),
                            "evidence": "Different response when accessing another user's data",
                            "severity": "High",
                            "remediation": {
                                "primary_fix": "Verify user identity before returning resources.",
                                "rbac": "Implement Role-Based Access Control.",
                                "session_validation": "Ensure session matches resource owner.",
                                "server_checks": "Perform authorization checks on server."
                            }
                        })

                except requests.RequestException:
                    continue

    return findings


def test_vertical_privilege_escalation(session, base_url):
    findings = []

    admin_paths = [
        "/admin",
        "/admin/dashboard",
        "/admin/users",
        "/admin/panel"
    ]

    for path in admin_paths:

        full_url = base_url.rstrip("/") + path

        try:
            response = session.get(full_url)

            if response.status_code == 200:

                findings.append({
                    "type": "Vertical Privilege Escalation",
                    "url": full_url,
                    "evidence": "Admin endpoint accessible without proper role",
                    "severity": "Critical",
                    "remediation": {
                        "primary_fix": "Restrict admin routes to authorized roles only.",
                        "rbac": "Implement Role-Based Access Control.",
                        "abac": "Use Attribute-Based Access Control.",
                        "authorization": "Check user role before granting access."
                    }
                })

        except requests.RequestException:
            continue

    return findings