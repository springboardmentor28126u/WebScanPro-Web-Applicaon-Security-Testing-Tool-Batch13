import requests
import json

session = requests.Session()

SQL_ERRORS = [
    "you have an error in your sql syntax",
    "warning: mysql",
    "unclosed quotation mark",
    "quoted string not properly terminated",
    "sqlstate",
    "mysql_fetch"
]


def load_payloads():
    with open("payloads/sql_payloads.txt", "r") as f:
        return [line.strip() for line in f.readlines()]


def analyze_response(response):
    for error in SQL_ERRORS:
        if error.lower() in response.text.lower():
            return True
    return False


def test_url(url):
    payloads = load_payloads()
    vulnerabilities = []   

    for payload in payloads:
        test_url = url + payload

        try:
            response = session.get(test_url)

            if analyze_response(response):
                print(f"[!] Vulnerable: {url}")
                vulnerabilities.append({
                    "url": url,
                    "payload": payload,
                    "type": "SQL Injection"
                })

        except Exception as e:
            print("Error:", e)

  
    with open("reports/sql_report.json", "w") as f:
        json.dump(vulnerabilities, f, indent=4)

    return vulnerabilities
