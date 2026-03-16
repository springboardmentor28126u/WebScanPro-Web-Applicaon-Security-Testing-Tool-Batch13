def test_default_credentials(base_url, requester):

    login_url = base_url + "login.php"

    common_credentials = [
        ("admin", "admin"),
        ("admin", "password"),
        ("root", "root"),
        ("test", "test"),
        ("user", "password")
    ]

    vulnerabilities = []

    for username, password in common_credentials:

        payload = {
            "username": username,
            "password": password,
            "Login": "Login"
        }

        response = requester.session.post(login_url, data=payload)

        if "Logout" in response.text:

            vulnerabilities.append({
                "type": "Weak Credentials",
                "url": login_url,
                "severity": "High",
                "description": f"Login successful with {username}/{password}",
                "fix": "Disable default accounts and enforce strong passwords."
            })

            break

    return vulnerabilities



def simulate_bruteforce(base_url, requester):

    login_url = base_url + "login.php"

    passwords = [
        "123456",
        "password",
        "admin",
        "letmein",
        "qwerty"
    ]

    vulnerabilities = []

    for pwd in passwords:

        payload = {
            "username": "admin",
            "password": pwd,
            "Login": "Login"
        }

        response = requester.session.post(login_url, data=payload)

        if "Logout" in response.text:

            vulnerabilities.append({
                "type": "Brute Force Possible",
                "url": login_url,
                "severity": "High",
                "description": f"Password guessed: {pwd}",
                "fix": "Implement account lockout and rate limiting."
            })

            break

    return vulnerabilities



def check_cookie_security(requester):

    vulnerabilities = []

    cookies = requester.session.cookies

    for cookie in cookies:

        if not cookie.secure:

            vulnerabilities.append({
                "type": "Insecure Cookie",
                "severity": "Medium",
                "description": f"{cookie.name} cookie missing Secure flag",
                "fix": "Enable Secure and HttpOnly flags."
            })

    return vulnerabilities



def test_session_fixation(base_url, requester):

    vulnerabilities = []

    session_before = requester.session.cookies.get_dict()

    requester.login(base_url)

    session_after = requester.session.cookies.get_dict()

    if session_before == session_after:

        vulnerabilities.append({
            "type": "Session Fixation",
            "severity": "High",
            "description": "Session ID not regenerated after login.",
            "fix": "Regenerate session ID after authentication."
        })

    return vulnerabilities