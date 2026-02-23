import json
from crawler import extract_forms

target_urls = [
    "http://localhost/dvwa/login.php",
    "http://localhost/dvwa/vulnerabilities/sqli/",
    "http://localhost/dvwa/vulnerabilities/xss_r/",
    "http://localhost/dvwa/vulnerabilities/xss_s/"
]

scan_data = {}

for url in target_urls:
    forms = extract_forms(url)
    scan_data[url] = forms

with open("scan_results.json", "w") as file:
    json.dump(scan_data, file, indent=4)

print("Scanning Completed ✅")

print ("metadata saved successfully")



