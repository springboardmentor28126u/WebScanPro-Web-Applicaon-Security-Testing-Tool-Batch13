import requests
from bs4 import BeautifulSoup
from scanner.crawler import crawl
from scanner.sqli_scanner import scan_sql
from scanner.xss_scanner import scan_xss
import json
import os

DVWA_URL = "http://localhost:8080"
LOGIN_URL = DVWA_URL + "/login.php"


def check_connection():
    try:
        response = requests.get(DVWA_URL, timeout=5)
        if response.status_code == 200:
            print("[+] DVWA connected successfully")
            return True
    except:
        print("[-] Failed to connect to DVWA")
    return False



def dvwa_login():
    session = requests.Session()

    try:
        response = session.get(LOGIN_URL)
        soup = BeautifulSoup(response.text, "html.parser")
        token_input = soup.find("input", {"name": "user_token"})

        if token_input is None:
            print("[-] Could not find user_token")
            return None

        user_token = token_input.get("value")

        login_data = {
            "username": "admin",
            "password": "password",
            "user_token": user_token,
            "Login": "Login"
        }

        response = session.post(LOGIN_URL, data=login_data)

        if "Logout" in response.text:
            print("[+] Logged into DVWA successfully")
            return session
        else:
            print("[-] Login failed")
            return None

    except Exception as e:
        print(f"[-] Login error: {e}")
        return None



if __name__ == "__main__":

    if check_connection():

        session = dvwa_login()

        if session:

            results = crawl(DVWA_URL, session)

            print("\n[+] Crawl finished")
            print(f"[+] Total Forms Found: {len(results)}")

            os.makedirs("reports", exist_ok=True)

            with open("reports/results.json", "w") as file:
                json.dump(results, file, indent=4)

           
            sqli_results = scan_sql(session, results)

   
            xss_results = scan_xss(session, results)

            all_vulnerabilities = sqli_results + xss_results

            final_report = {
                "target": DVWA_URL,
                "total_vulnerabilities": len(all_vulnerabilities),
                "vulnerabilities": all_vulnerabilities
            }

            with open("reports/vulnerability_report.json", "w") as file:
                json.dump(final_report, file, indent=4)

            print("\n[+] Vulnerability report saved.")
            print(f"[+] Total Vulnerabilities Found: {len(all_vulnerabilities)}")