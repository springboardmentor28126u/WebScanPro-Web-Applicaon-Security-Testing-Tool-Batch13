import requests
from bs4 import BeautifulSoup
from scanner.config import LOGIN_URL

# Common passwords attackers try first
COMMON_PASSWORDS = ["password", "123456", "admin", "letmein", "qwerty", "password1"]

def brute_force(login_url, username, passwords=COMMON_PASSWORDS):
    findings = []
    for pwd in passwords:
        session = requests.Session()     # Fresh session for each attempt
        r = session.get(login_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        token_tag = soup.find('input', {'name': 'user_token'})

        data = {'username': username, 'password': pwd, 'Login': 'Login'}
        if token_tag: data['user_token'] = token_tag['value']

        resp = session.post(login_url, data=data)

        # "Welcome" or "logout" only appear when logged in = weak creds found
        if "Welcome" in resp.text or "logout" in resp.text.lower():
            findings.append({
                'username': username, 'password': pwd,
                'type': 'Weak Credentials', 'severity': 'HIGH',
                'url': login_url, 'parameter': 'password', 'payload': pwd
            })
            print(f"  [VULN] Weak credentials: {username}:{pwd}")
            break   # Found working password — stop trying more
        else:
            print(f"  Tried {username}:{pwd} - failed")
    return findings

def check_cookie_security(session, url):
    session.get(url)
    issues = []
    for cookie in session.cookies:
        # Secure flag — cookie only sent over HTTPS, not plain HTTP
        if not cookie.secure:
            issues.append({'type': 'Insecure Cookie', 'parameter': cookie.name,
                           'payload': 'Missing Secure flag', 'url': url,
                           'issue': 'Missing Secure flag', 'severity': 'MEDIUM'})
        # HttpOnly flag — cookie cannot be read by JavaScript (prevents XSS theft)
        if not cookie.has_nonstandard_attr('HttpOnly'):
            issues.append({'type': 'Insecure Cookie', 'parameter': cookie.name,
                           'payload': 'Missing HttpOnly flag', 'url': url,
                           'issue': 'Missing HttpOnly flag', 'severity': 'MEDIUM'})
    return issues