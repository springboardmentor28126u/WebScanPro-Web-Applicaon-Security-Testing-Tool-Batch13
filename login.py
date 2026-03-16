import requests
from bs4 import BeautifulSoup

BASE_URL = "http://localhost:8080/dvwa/"

def login():
    # Session created inside function — not as a global variable
    session = requests.Session()
    

    login_url = BASE_URL + "login.php"

    # GET login page to extract CSRF token
    response = session.get(login_url)
    soup = BeautifulSoup(response.text, "html.parser")
    token = soup.find("input", {"name": "user_token"})["value"]

    data = {
        "username": "admin",
        "password": "password",
        "Login": "Login",
        "user_token": token
    }

    session.post(login_url, data=data)

    print("✅ Logged into DVWA")

    # Return session and login_url only — token NOT returned
    # because brute force fetches its own fresh token each attempt
    return session, login_url


def set_security_low(session):
    security_url = BASE_URL + "security.php"

    response = session.get(security_url)
    soup = BeautifulSoup(response.text, "html.parser")
    token = soup.find("input", {"name": "user_token"})["value"]

    data = {
        "security": "low",
        "seclev_submit": "Submit",
        "user_token": token
    }

    session.post(security_url, data=data)

    print("🔓 DVWA Security Level set to LOW")