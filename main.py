import requests
from urllib.parse import urlparse

from scanner.crawler import login_dvwa, crawl
from scanner.extractor import extract_forms
from scanner.report_generator import generate_html_report
from scanner.sqli_tester import test_sqli
from scanner.xss_tester import test_xss, test_xss_url_params

from scanner.auth_tester import (
    test_default_credentials,
    test_bruteforce,
    test_session_security,
    test_session_fixation
)

from scanner.idor_tester import (
    test_idor,
    test_horizontal_privilege_escalation,
    test_vertical_privilege_escalation
)

from scanner.storage import save_report, save_metadata


def main():

    start_url = "http://localhost/dvwa/"
    login_url = "http://localhost/dvwa/login.php"
    base_domain = urlparse(start_url).netloc

    # ==============================
    # LOGIN
    # ==============================
    session = login_dvwa()
    if not session:
        return

    # ==============================
    # CRAWLING
    # ==============================
    print("\n[+] Crawling site...\n")

    visited = set()
    links = crawl(start_url, base_domain, session, visited)

    all_pages = [start_url] + links

    for page in all_pages:
        print("Scanning:", page)

    print(f"\nTotal pages found: {len(all_pages)}")

    save_metadata(all_pages, "data/targets.json")

    # ==============================
    # FORM EXTRACTION
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
    # SQL INJECTION TESTING
    # ==============================
    print("\nStarting Advanced SQL Injection Testing...\n")

    sqli_results = test_sqli(session, target_data)

    if sqli_results:
        print("\nPotential SQL Injection Vulnerabilities Found:\n")

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
    # XSS TESTING
    # ==============================
    print("\nStarting XSS Testing...\n")

    xss_form_results = test_xss(session, target_data)
    xss_url_results = test_xss_url_params(session, target_data)

    all_xss_results = xss_form_results + xss_url_results

    if all_xss_results:
        print("\nPotential XSS Vulnerabilities Found:\n")

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
    # AUTHENTICATION TESTING
    # ==============================
    print("\nStarting Authentication Testing...\n")

    auth_results = test_default_credentials(login_url)
    brute_results = test_bruteforce(login_url)
    session_results = test_session_security(session, start_url)
    fixation_results = test_session_fixation(session, login_url)

    auth_all = auth_results + brute_results + session_results + fixation_results

    # ==============================
    # ACCESS CONTROL / IDOR TESTING
    # ==============================
    print("\nStarting Access Control and IDOR Testing...\n")

    idor_results = test_idor(session, all_pages)
    horizontal_results = test_horizontal_privilege_escalation(session, all_pages)
    vertical_results = test_vertical_privilege_escalation(session)

    access_results = idor_results + horizontal_results + vertical_results

    # ==============================
    # SAVE REPORT
    # ==============================
    all_results = {
        "sqli": sqli_results,
        "xss": all_xss_results,
        "authentication": auth_all,
        "access_control": access_results
    }

    save_report(all_results, "data/vulnerabilities.json")

    from scanner.report_generator import generate_html_report, generate_pdf

    generate_html_report("data/vulnerabilities.json")
    generate_pdf()

    # ==============================
    # FINAL SUMMARY
    # ==============================
    if not sqli_results and not all_xss_results and not auth_all and not access_results:
        print("\nNo vulnerabilities detected.")




if __name__ == "__main__":
    main()