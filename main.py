from request_handler import RequestHandler
from sql_injection import SQLScanner
from crawler import crawl
import json

def main():
    base_url = "http://127.0.0.1/dvwa/"

    print("[*] Web Scan Pro Starting...")

    request_handler = RequestHandler()

    if not request_handler.login(base_url):
        print("[-] Login failed. Exiting.")
        return

    print("[+] Login successful!")

    request_handler.set_security_low(base_url)
    print("[+] Security level set to LOW")

    # Step 1: Crawl and Extract Forms
    forms = crawl(base_url, request_handler)

    # Step 2: Run SQL Injection Scan

    scanner = SQLScanner(request_handler.session)

    vulnerabilities = []

    for form in forms:
        if form["method"] and form["method"].lower() == "get":
            for input_field in form["inputs"]:
                if input_field["type"] == "text" and input_field["name"]:
                    vulns = scanner.test_get_parameter(
                        form["page"],
                        input_field["name"]
                    )
                    vulnerabilities.extend(vulns)

    # Step 3: Save Everything in ONE Structured Report
    final_report = {
        "total_forms": len(forms),
        "forms": forms,
        "total_vulnerabilities": len(vulnerabilities),
        "vulnerabilities": vulnerabilities
    }

    with open("scan_results.json", "w") as f:
        json.dump(final_report, f, indent=4)

    print("\nScan Completed Successfully!")
    print(json.dumps(final_report, indent=4))

if __name__ == "__main__":
    main()