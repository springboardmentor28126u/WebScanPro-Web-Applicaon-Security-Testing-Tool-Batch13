from login import login, set_security_low
from bruteforce_scanner import brute_force_login
from sqli_tester import run_sqli_scan
from xss_scanner import run_xss_scan
from privilege_escalation_scanner import test_horizontal_privilege_escalation
from report_generator import generate_report


def main():

    print("🚀 Starting WebScanPro Scanner...\n")

    # Step 1: Login to DVWA
    session, login_url = login()

    # Step 2: Set DVWA security level to LOW
    set_security_low(session)

    print("\n----------------------------\n")

    # Week 3 - SQL Injection Scan
    sqli_results = run_sqli_scan(session)

    print("\n----------------------------\n")

    # Week 4 - XSS Scan
    xss_results = run_xss_scan(session)

    print("\n----------------------------\n")

    # Week 5 - Brute Force Login Test
    brute_force_results = brute_force_login(session, login_url)

    print("\n----------------------------\n")

    # Week 6 - Privilege Escalation / IDOR Test
    privilege_results = test_horizontal_privilege_escalation(session)

    print("\n----------------------------\n")

    # Generate Final Report
    generate_report(brute_force_results, sqli_results, xss_results, privilege_results)

    print("\n✅ Scan Completed Successfully")


if __name__ == "__main__":
    main()