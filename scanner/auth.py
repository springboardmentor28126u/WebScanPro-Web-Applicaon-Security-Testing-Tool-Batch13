import requests
from bs4 import BeautifulSoup
from scanner.config import LOGIN_URL, USERNAME, PASSWORD

def get_session(login_url=LOGIN_URL, username=USERNAME, password=PASSWORD):
    session = requests.Session()

    # Step 1: Get login page
    r = session.get(login_url)
    soup = BeautifulSoup(r.text, "html.parser")

    token = soup.find("input", {"name": "user_token"})["value"]

    # Step 2: Login
    payload = {
        "username": username,
        "password": password,
        "Login": "Login",
        "user_token": token
    }

    login = session.post(login_url, data=payload)

    # Step 3: Set DVWA security
    session.cookies.set("security", "low")

    # Step 4: Verify login by accessing a protected page
    check = session.get("http://localhost:8081/vulnerabilities/")

    if "login.php" in check.url:
        print("  [ERROR] Login failed! Check config.py credentials")
    else:
        print("  [OK] Session active - logged in successfully")

    return session