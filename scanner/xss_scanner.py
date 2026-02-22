def scan_xss(session, forms):
    print("\n[+] Starting XSS Scan...")
    vulnerabilities = []

    payload = "<script>alert(1)</script>"

    for form in forms:
        if "vulnerabilities/xss_r" not in form["action"]:
            continue

        action_url = form["action"].split("#")[0]

        for input_field in form["inputs"]:
            if input_field["type"] == "text" and input_field["name"]:

                data = {
                    input_field["name"]: payload
                }

                try:
                    response = session.get(action_url, params=data)

                    if payload in response.text:
                        print(f"[!!!] XSS Found at {action_url}")

                        vulnerabilities.append({
                            "type": "Reflected XSS",
                            "url": action_url,
                            "parameter": input_field["name"],
                            "payload": payload,
                            "severity": "Medium"
                        })

                except:
                    continue

    return vulnerabilities