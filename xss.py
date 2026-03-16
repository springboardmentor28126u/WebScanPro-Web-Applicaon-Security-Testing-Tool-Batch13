def test_xss(requester, form):
    vulnerabilities = []

    payload = "<script>alert('XSS')</script>"

    page = form["page"]
    method = form["method"].lower()
    inputs = form["inputs"]

    for input_field in inputs:
        if input_field["type"] in ["text", "search"] and input_field["name"]:

            data = {}
            for field in inputs:
                if field["name"]:
                    data[field["name"]] = payload

            try:
                if method == "get":
                    response = requester.session.get(page, params=data)
                else:
                    response = requester.session.post(page, data=data)

                if payload in response.text:
                    vulnerabilities.append({
                        "url": page,
                        "parameter": input_field["name"],
                        "type": "Reflected XSS",
                        "severity": "High",
                        "fix": "Sanitize user input and use output encoding."
                    })

            except:
                pass

    return vulnerabilities