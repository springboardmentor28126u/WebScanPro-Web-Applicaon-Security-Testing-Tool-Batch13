import requests
from bs4 import BeautifulSoup

BASE_URL = "http://127.0.0.1:8080/dvwa"
LOGIN_URL = BASE_URL + "/login.php"

USERNAME = "admin"
PASSWORD = "password"

def login():
    session = requests.Session()

    # ADD THIS IMPORTANT HEADER
    session.headers.update({
        "User-Agent": "Mozilla/5.0",
        "Referer": LOGIN_URL
    })

    print("🔹 STEP 1: Getting login page...")
    response = session.get(LOGIN_URL)

    print("GET Status Code:", response.status_code)
    print("Cookies after GET:", session.cookies)

    soup = BeautifulSoup(response.text, "html.parser")

    token_input = soup.find("input", {"name": "user_token"})
    if not token_input:
        print("❌ CSRF Token not found.")
        return

    token = token_input["value"]
    print("Extracted CSRF Token:", token)

    print("\n🔹 STEP 2: Sending login POST request...")

    login_data = {
        "username": USERNAME,
        "password": PASSWORD,
        "Login": "Login",
        "user_token": token
    }

    response = session.post(
        LOGIN_URL,
        data=login_data,
        headers={"Referer": LOGIN_URL}   # VERY IMPORTANT
    )

    print("POST Status Code:", response.status_code)
    print("Cookies after POST:", session.cookies)

    if "Logout" in response.text:
        print("\n✅ Login Successful!")
    else:
        print("\n❌ Login Failed!")
        print(response.text[:300])


if __name__ == "__main__":
    login()