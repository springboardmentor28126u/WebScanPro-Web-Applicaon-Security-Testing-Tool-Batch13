import requests
from bs4 import BeautifulSoup

class RequestHandler:
    def set_security_low(self, base_url):
        security_url = f"{base_url}security.php"

        # Step 1: Get security page to extract CSRF token
        response = self.session.get(security_url)
        soup = BeautifulSoup(response.text, "html.parser")

        token_input = soup.find("input", attrs={"name": "user_token"})
        if not token_input:
            print("[-] Security CSRF token not found.")
            return

        user_token = token_input.get("value")

        # Step 2: Send POST request with token
        payload = {
            "security": "low",
            "seclev_submit": "Submit",
            "user_token": user_token
        }

        self.session.post(security_url, data=payload)

        self.session.post(security_url, data=payload)
        
    def __init__(self):
        self.session = requests.Session()

    def login(self, base_url):
        login_url = f"{base_url}/login.php"

        try:
            response = self.session.get(login_url)
            soup = BeautifulSoup(response.text, "html.parser")

            token_input = soup.find("input", attrs={"name": "user_token"})
            if not token_input:
                print("[-] CSRF token not found.")
                return False

            user_token = token_input.get("value")

            payload = {
                "username": "admin",
                "password": "password",
                "user_token": user_token,
                "Login": "Login"
            }

            login_response = self.session.post(login_url, data=payload)

            # ✅ Correct success check
            if "Logout" in login_response.text:
                print("[+] Login successful!")
                return True
            else:
                print("[-] Login failed.")
                return False

        except Exception as e:
            print("[!] Login error:", e)
            return False