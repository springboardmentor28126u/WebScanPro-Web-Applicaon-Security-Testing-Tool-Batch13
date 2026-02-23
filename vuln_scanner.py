import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from payloads import SQLI_PAYLOADS, XSS_PAYLOADS, SQL_ERRORS

# Configuration for your Docker DVWA
TARGET_URL = "http://localhost:8080/vulnerabilities/sqli/" 
# IMPORTANT: You'll need your actual session cookie from the browser
COOKIES = {"PHPSESSID": "78478o49ctf7h4npjmkmcer7d3", "security": "low"}

def scan_vulnerabilities(url):
    print(f"--- [WebScanPro] Milestone 2: Starting Vulnerability Scan ---")
    
    # 1. Test for SQL Injection (GET based)
    for payload in SQLI_PAYLOADS:
        test_url = f"{url}?id={payload}&Submit=Submit#"
        print(f"[*] Testing SQLi: {payload}")
        
        response = requests.get(test_url, cookies=COOKIES)
        
        for error in SQL_ERRORS:
            if error in response.text.lower():
                print(f"  [!] VULNERABLE (SQLi) found at: {url}")
                break

    # 2. Test for XSS (Reflected)
    xss_url = "http://localhost:8080/vulnerabilities/xss_r/"
    for payload in XSS_PAYLOADS:
        print(f"[*] Testing XSS: {payload}")
        params = {"name": payload}
        response = requests.get(xss_url, params=params, cookies=COOKIES)
        
        if payload in response.text:
            print(f"  [!] VULNERABLE (XSS) found at: {xss_url}")

if __name__ == "__main__":
    scan_vulnerabilities(TARGET_URL)