import requests
import json

print("\nAccess Control & IDOR Testing")
print("------------------------------\n")

results = []

urls = [
"http://localhost/dvwa/vulnerabilities/fi/?page=file1.php",
"http://localhost/dvwa/vulnerabilities/fi/?page=../fi/file2.php",
"http://localhost/dvwa/vulnerabilities/idor/?id=3"
]

for url in urls:
    response = requests.get(url)

    if "Hello" in response.text or "password" in response.text:
        print("[!] Possible File Inclusion Found:", url)

        results.append({
            "vulnerability": "Local File Inclusion",
            "url_tested": url,
            "severity": "High",
            "status": "Vulnerable"
        })

    else:
        print("[OK] Safe:", url)

        results.append({
            "vulnerability": "Local File Inclusion",
            "url_tested": url,
            "severity": "Low",
            "status": "Not Vulnerable"
        })

# Save JSON report
with open("idor_report.json", "w") as file:
    json.dump(results, file, indent=4)

print("\nJSON report generated: idor_report.json")