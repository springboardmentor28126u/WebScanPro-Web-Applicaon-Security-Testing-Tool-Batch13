import requests
import urllib.parse
import json

# List of payloads to test
payloads = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "<svg onload=alert('XSS')>"
]

# List of URLs to test
# Add your own localhost / test server URLs here
urls = [
    "http://127.0.0.1:5000/search?q="
]

vulnerable_results = []

for base_url in urls:
    for payload in payloads:
        # Encode payload so it's safe in URL
        encoded_payload = urllib.parse.quote(payload)
        test_url = f"{base_url}{encoded_payload}"

        try:
            response = requests.get(test_url, timeout=10)
            body = response.text

            # Check if our payload shows up unencoded in the HTTP response
            if payload in body:
                print(f"[VULNERABLE] {test_url}")
                vulnerable_results.append({
                    "url": test_url,
                    "payload": payload,
                    "status_code": response.status_code
                })
            else:
                print(f"[OK] Not vulnerable: {test_url}")

        except Exception as e:
            print(f"Error requesting {test_url}: {e}")

# Save a report
with open("xss_report.json", "w") as f:
    json.dump(vulnerable_results, f, indent=2)

print("Scan complete — results saved to xss_report.json")
