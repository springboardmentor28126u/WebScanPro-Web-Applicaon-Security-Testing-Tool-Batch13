import requests
from bs4 import BeautifulSoup

class RequestHandler:
    def __init__(self):
        self.session = requests.Session()

    def login(self, base_url):
        login_url = f"{base_url}/login.php"

        try:
            # Get login page first (to extract CSRF token)
            response = self.session.get(login_url)
            soup = BeautifulSoup(response.text, "html.parser")

            token_input = soup.find("input", {"name": "user_token"})
            if not token_input:
                print("[-] CSRF token not found.")
                return False

            user_token = token_input["value"]

            payload = {
                "username": "admin",
                "password": "password",
                "user_token": user_token,
                "Login": "Login"
            }

            login_response = self.session.post(login_url, data=payload)

            if "Login failed" in login_response.text:
                return False

            return True

        except Exception as e:
            print("[!] Login error:", e)
            return False
