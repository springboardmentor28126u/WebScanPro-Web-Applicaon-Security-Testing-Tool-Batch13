import requests
from bs4 import BeautifulSoup

BASE_URL = "http://localhost:8080/dvwa"
LOGIN_URL = BASE_URL + "/login.php"

USERNAME = "admin"
PASSWORD = "password"

def login():
    session = requests.Session()

    # Step 1: Get login page
    response = session.get(LOGIN_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    token_input = soup.find("input", {"name": "user_token"})
    if not token_input:
        print("❌ Token not found")
        return None

    token = token_input["value"]

    # Step 2: Send login request
    login_data = {
        "username": USERNAME,
        "password": PASSWORD,
        "Login": "Login",
        "user_token": token
    }

    response = session.post(LOGIN_URL, data=login_data)

    # Step 3: Verify login
    if "Logout" in response.text:
        print("✅ Login Successful")
        return session
    else:
        print("❌ Login Failed")
        print(response.text[:500])  # Print part of page for debugging
        return None


if __name__ == "__main__":
    login()