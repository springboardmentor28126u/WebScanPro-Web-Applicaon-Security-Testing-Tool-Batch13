def test_horizontal_privilege(base_url, requester):

    vulnerabilities = []

    test_urls = [
        base_url + "vulnerabilities/weak_id/?id=1",
        base_url + "vulnerabilities/weak_id/?id=2",
        base_url + "vulnerabilities/weak_id/?id=3"
    ]

    responses = []

    for url in test_urls:

        response = requester.session.get(url)

        responses.append(response.text)

    if len(set(responses)) > 1:

        vulnerabilities.append({
            "type": "Horizontal Privilege Escalation",
            "severity": "High",
            "description": "Different user data accessible via ID parameter manipulation.",
            "fix": "Implement proper authorization checks."
        })

    return vulnerabilities



def test_vertical_privilege(base_url, requester):

    vulnerabilities = []

    admin_urls = [
        base_url + "admin",
        base_url + "admin/dashboard",
        base_url + "admin/settings"
    ]

    for url in admin_urls:

        response = requester.session.get(url)

        if response.status_code == 200:

            vulnerabilities.append({
                "type": "Vertical Privilege Escalation",
                "url": url,
                "severity": "High",
                "description": "Admin endpoint accessible without proper authorization.",
                "fix": "Restrict admin endpoints using role-based access control."
            })

    return vulnerabilities



def test_idor(base_url, requester):

    vulnerabilities = []

    for i in range(1, 5):

        url = f"{base_url}vulnerabilities/weak_id/?id={i}"

        response = requester.session.get(url)

        if "User ID" in response.text or "First name" in response.text:

            vulnerabilities.append({
                "type": "IDOR (Insecure Direct Object Reference)",
                "url": url,
                "severity": "High",
                "description": "Object accessible by modifying ID parameter.",
                "fix": "Validate object ownership on server side."
            })

    return vulnerabilities