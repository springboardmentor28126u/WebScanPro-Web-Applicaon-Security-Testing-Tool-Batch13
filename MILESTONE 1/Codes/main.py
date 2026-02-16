import requests
from bs4 import BeautifulSoup
from scanner.crawler import crawl
import json
import os


DVWA_URL = "http://localhost:8081"
LOGIN_URL = DVWA_URL + "/login.php"

def check_connection():
    try:
        response = requests.get(DVWA_URL, timeout=5)
        if response.status_code == 200:
            print("[+] DVWA connected successfully")
            return True
    except Exception:
        print("[-] Failed to connect")
    return False


def dvwa_login():
    session = requests.Session()
    try:
        response = session.get(LOGIN_URL)
        soup = BeautifulSoup(response.text, "html.parser")
        token_input = soup.find("input", {"name": "user_token"})

        if token_input is None:
            print("[-] Could not find user_token in login page")
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

            # ---------- JSON SAVE PART ----------
            os.makedirs("reports", exist_ok=True)

            output_data = {
                "target": DVWA_URL,
                "total_forms": len(results),
                "forms": results
            }

            with open("reports/results.json", "w") as file:
                json.dump(output_data, file, indent=4)

            print("[+] Results saved to reports/results.json")

            for index, form in enumerate(results, start=1):
                print(f"\nForm #{index}")
                print(f"Action : {form['action']}")
                print(f"Method : {form['method']}")
                print("Inputs :")
                
                for inp in form["inputs"]:
                    print(f"   - Name: {inp['name']} | Type: {inp['type']}")
                
                print("-" * 50)

