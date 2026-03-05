import requests
from urllib.parse import urlparse
from scanner.crawler import login_dvwa, crawl
from scanner.extractor import extract_forms
from scanner.sqli_tester import test_sqli
from scanner.xss_tester import test_xss, test_xss_url_params
from scanner.storage import save_report


def main():
    start_url = "http://localhost/dvwa/"
    base_domain = urlparse(start_url).netloc

    # ==============================
    # 1️⃣ LOGIN
    # ==============================
    session = login_dvwa()
    if not session:
        return

    # ==============================
    # 2️⃣ CRAWLING
    # ==============================
    print("\n[+] Crawling site...\n")

    visited = set()
    links = crawl(start_url, base_domain, session, visited)

    all_pages = [start_url] + links

    for page in all_pages:
        print("Scanning:", page)

    print(f"\nTotal pages found: {len(all_pages)}")

    from scanner.storage import save_metadata

    save_metadata(all_pages, "data/targets.json")

    # ==============================
    # 3️⃣ FORM EXTRACTION
    # ==============================
    print("\n[+] Extracting forms...\n")

    target_data = []

    for page in all_pages:
        forms = extract_forms(page, session)

        if forms:
            target_data.append({
                "url": page,
                "forms": forms
            })

    # ==============================
    # 4️⃣ SQL INJECTION TESTING
    # ==============================
    print("\nStarting Advanced SQL Injection Testing...\n")

    sqli_results = test_sqli(session, target_data)

    print("\nTesting Complete.\n")

    if sqli_results:
        print("Potential SQL Injection Vulnerabilities Found:\n")

        for v in sqli_results:
            print("Type:", v["type"])
            print("URL:", v["url"])
            print("Parameter:", v["parameter"])

            if "payload" in v:
                print("Payload Used:", v["payload"])

            if "length_difference" in v:
                print("Length Difference:", v["length_difference"])

            print("Remediation Suggestions:")
            for _, value in v.get("remediation", {}).items():
                print(" -", value)

            print("-" * 60)
    else:
        print("No SQL Injection patterns detected.")

    # ==============================
    # 5️⃣ XSS TESTING
    # ==============================
    print("\nStarting XSS Testing...\n")

    xss_form_results = test_xss(session, target_data)
    xss_url_results = test_xss_url_params(session, target_data)

    all_xss_results = xss_form_results + xss_url_results

    if all_xss_results:
        print("Potential XSS Vulnerabilities Found:\n")

        for v in all_xss_results:
            print("Type:", v["type"])
            print("URL:", v["url"])
            print("Parameter:", v.get("parameter"))
            print("Severity:", v.get("severity", "Unknown"))

            if "payload" in v:
                print("Payload Used:", v["payload"])

            print("Remediation Suggestions:")
            for _, value in v.get("remediation", {}).items():
                print(" -", value)

            print("-" * 60)
    else:
        print("No XSS patterns detected.")

    # ==============================
    # 6️⃣ SAVE REPORT
    # ==============================
    all_results = {
        "sqli": sqli_results,
        "xss": all_xss_results
    }

    save_report(all_results, "data/vulnerabilities.json")

    # ==============================
    # 7️⃣ FINAL SUMMARY
    # ==============================
    if not sqli_results and not all_xss_results:
        print("\nNo vulnerabilities detected.")


if __name__ == "__main__":
    main()