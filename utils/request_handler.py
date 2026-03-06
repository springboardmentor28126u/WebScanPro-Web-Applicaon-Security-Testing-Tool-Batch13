import requests

class RequestHandler:
    def __init__(self):
        self.session = requests.Session()

    def login_dvwa(self, base_url):
        login_url = f"{base_url}/login.php"

        login_data = {
            "username": "admin",
            "password": "password",
            "Login": "Login"
        }

        response = self.session.post(login_url, data=login_data)

        if "Logout" in response.text:
            print("[+] DVWA Login Successful")
            return True
        else:
            print("[-] DVWA Login Failed")
            return False
