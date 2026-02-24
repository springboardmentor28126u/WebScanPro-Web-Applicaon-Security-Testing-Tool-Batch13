from scanner.auth import get_session

session = get_session()

r = session.get("http://localhost/vulnerabilities/sqli/", params={"id": "'", "Submit": "Submit"})

print("=== FULL RESPONSE LENGTH ===")
print(len(r.text))
print("=== FULL RESPONSE ===")
print(r.text)