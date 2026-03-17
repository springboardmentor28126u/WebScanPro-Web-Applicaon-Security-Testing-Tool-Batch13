import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


# Common IDs to test when modifying parameters
TEST_IDS = ["1", "2", "3", "4", "5", "10", "100"]


def modify_parameter(url, param, new_value):
    """
    Modify a parameter in the URL and return the new URL
    """

    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    params[param] = new_value

    new_query = urlencode(params, doseq=True)

    new_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment
    ))

    return new_url


def test_idor(session, urls):
    """
    Test for IDOR by modifying parameters like id, user_id etc
    """

    findings = []

    for url in urls:

        parsed = urlparse(url)
        params = parse_qs(parsed.query)

        if not params:
            continue

        for param in params:

            if "id" in param.lower():

                for test_id in TEST_IDS:

                    modified_url = modify_parameter(url, param, test_id)

                    try:
                        response = session.get(modified_url)

                        if response.status_code == 200:

                            findings.append({
                                "type": "Potential IDOR",
                                "url": url,
                                "parameter": param,
                                "tested_value": test_id,
                                "issue": "Application returned valid response for modified object ID",
                                "severity": "High",
                                "remediation": {
                                    "primary_fix": "Validate user authorization before returning object data.",
                                    "rbac": "Implement Role-Based Access Control (RBAC).",
                                    "abac": "Use Attribute-Based Access Control (ABAC) for fine-grained permissions.",
                                    "direct_reference": "Avoid exposing direct object identifiers in URLs.",
                                    "server_validation": "Verify ownership of objects on the server side."
                                }
                            })

                    except requests.RequestException:
                        continue

    return findings


def test_horizontal_privilege_escalation(session, urls):
    """
    Simulate horizontal privilege escalation by accessing
    objects belonging to other users
    """

    findings = []

    for url in urls:

        if "user" in url or "account" in url:

            for test_id in TEST_IDS:

                modified_url = f"{url}?user_id={test_id}"

                try:
                    response = session.get(modified_url)

                    if response.status_code == 200:

                        findings.append({
                            "type": "Horizontal Privilege Escalation",
                            "url": modified_url,
                            "tested_user_id": test_id,
                            "severity": "High",
                            "issue": "User may access another user's data",
                            "remediation": {
                                "primary_fix": "Verify user identity before returning resources.",
                                "rbac": "Implement Role-Based Access Control.",
                                "session_validation": "Ensure user session matches resource owner.",
                                "server_checks": "Perform authorization checks on the server."
                            }
                        })

                except requests.RequestException:
                    continue

    return findings


def test_vertical_privilege_escalation(session):
    """
    Attempt to access admin resources as a normal user
    """

    findings = []

    admin_paths = [
        "/admin",
        "/admin/dashboard",
        "/admin/users",
        "/admin/panel"
    ]

    for path in admin_paths:

        try:
            response = session.get(path)

            if response.status_code == 200:

                findings.append({
                    "type": "Vertical Privilege Escalation",
                    "url": path,
                    "severity": "Critical",
                    "issue": "Admin resource accessible without admin privileges",
                    "remediation": {
                        "primary_fix": "Restrict admin routes to authorized roles only.",
                        "rbac": "Implement Role-Based Access Control.",
                        "abac": "Use Attribute-Based Access Control for fine-grained policies.",
                        "authorization": "Check user role before granting access."
                    }
                })

        except requests.RequestException:
            continue

    return findings