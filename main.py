import requests
from urllib.parse import urlparse

from scanner.crawler import login_dvwa, crawl
from scanner.report_generator import generate_html_report, generate_pdf
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

    # ==============================
    # LOGIN
    # ==============================
    session = login_dvwa()
    if not session:
        return

    # ==============================
    # CRAWLING (NEW STRUCTURE)
    # ==============================
    print("\n[+] Crawling site...\n")

    target_data = crawl(start_url, session)

    # extract only URLs for IDOR + metadata
    all_pages = [page["url"] for page in target_data]

    for page in all_pages:
        print("Scanning:", page)

    print(f"\nTotal pages found: {len(all_pages)}")

    save_metadata(all_pages, "data/targets.json")

    # ==============================
    # SQL INJECTION
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
    # XSS
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
    # AUTH
    # ==============================
    print("\nStarting Authentication Testing...\n")

    auth_results = test_default_credentials(session, login_url)
    brute_results = test_bruteforce(session, login_url)
    session_results = test_session_security(session, start_url)
    fixation_results = test_session_fixation(session, login_url)

    auth_all = auth_results + brute_results + session_results + fixation_results

    if auth_all:
        print("\nAuthentication & Session Vulnerabilities Found:\n")

        for v in auth_all:
            print("Type:", v["type"])
            print("URL:", v.get("url"))

            if "username" in v:
                print("Username:", v["username"])
            if "password" in v:
                print("Password:", v["password"])

            if "cookie" in v:
                print("Cookie:", v["cookie"])

            if "issue" in v:
                print("Issue:", v["issue"])

            if "evidence" in v:
                print("Evidence:", v["evidence"])

            print("Severity:", v.get("severity", "Unknown"))

            print("Remediation Suggestions:")
            for _, value in v.get("remediation", {}).items():
                print(" -", value)

            print("-" * 60)
    else:
        print("No authentication vulnerabilities detected.")

    # ==============================
    # IDOR
    # ==============================
    print("\nStarting Access Control and IDOR Testing...\n")

    idor_results = test_idor(session, all_pages)
    horizontal_results = test_horizontal_privilege_escalation(session, all_pages)
    vertical_results = test_vertical_privilege_escalation(session, start_url)

    access_results = idor_results + horizontal_results + vertical_results

    if access_results:
        print("\nAccess Control & IDOR Vulnerabilities Found:\n")

        for v in access_results:
            print("Type:", v["type"])
            print("URL:", v["url"])

            if "parameter" in v:
                print("Parameter:", v["parameter"])

            if "tested_value" in v:
                print("Tested Value:", v["tested_value"])

            if "tested_user_id" in v:
                print("Tested User ID:", v["tested_user_id"])

            if "difference" in v:
                print("Response Difference:", v["difference"])

            if "evidence" in v:
                print("Evidence:", v["evidence"])

            print("Severity:", v.get("severity", "Unknown"))

            print("Remediation Suggestions:")
            for _, value in v.get("remediation", {}).items():
                print(" -", value)

            print("-" * 60)
    else:
        print("No access control vulnerabilities detected.")

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

    generate_html_report("data/vulnerabilities.json")
    generate_pdf()

    # ==============================
    # FINAL
    # ==============================
    if not sqli_results and not all_xss_results and not auth_all and not access_results:
        print("\nNo vulnerabilities detected.")


if __name__ == "__main__":
    main()