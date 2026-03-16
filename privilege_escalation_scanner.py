BASE_URL = "http://localhost:8080/dvwa/vulnerabilities/sqli/"


def test_horizontal_privilege_escalation(session):

    print("🔎 Testing Horizontal Privilege Escalation (IDOR)...\n")

    results = []

    # Mix of valid user IDs and non-existent IDs
    test_ids = [1, 2, 3, 99, 999]

    for user_id in test_ids:

        params = {
            "id": user_id,
            "Submit": "Submit"
        }

        response = session.get(BASE_URL, params=params)

        # Check if user data is returned in the response
        if "First name:" in response.text and "Surname:" in response.text:
            status = "Accessible"

            if user_id in [1, 2, 3]:
                severity = "Medium"   # Valid users — data exposed without auth check
            else:
                severity = "High"     # Non-existent ID returned data = critical IDOR

        else:
            status = "Not Found"
            severity = "Low"          # No data leaked for this ID

        print(f"[IDOR Test] id={user_id} -> {status} (Severity: {severity})")
        results.append((user_id, status, severity))

    return results