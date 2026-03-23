from login import login, set_security_low
from bruteforce_scanner import brute_force_login
from sqli_tester import run_sqli_scan
from xss_scanner import run_xss_scan
from privilege_escalation_scanner import (
    test_horizontal_privilege_escalation,
    test_vertical_privilege_escalation,
)
from session_module import run_session_scan
from report_generator import generate_report

from datetime import datetime


def calculate_risk_score(*modules):
    score = 0
    total = 0

    for module in modules:
        for item in module:
            severity = item[-1]

            if severity == "High":
                score += 3
            elif severity == "Medium":
                score += 2
            elif severity == "Low":
                score += 1

            total += 1

    if total == 0:
        return 0

    return round((score / (total * 3)) * 10, 2)


def main():

    print("🚀 Starting WebScanPro Scanner...\n")

    start_time = datetime.now()

    # Step 1: Login to DVWA
    session, login_url = login()

    # Step 2: Set DVWA security level to LOW
    set_security_low(session)

    print("\n----------------------------\n")

    # Week 3 — SQL Injection Scan
    sqli_results = run_sqli_scan(session)

    print("\n----------------------------\n")

    # Week 4 — XSS Scan
    xss_results = run_xss_scan(session)

    print("\n----------------------------\n")

    # Week 5 — Brute Force Login Test
    # Week 5 - Brute Force Login Test
    brute_force_all, brute_force_results = brute_force_login(session, login_url)

    print("\n----------------------------\n")

    # Week 5 — Session & Cookie Testing
    session_results = run_session_scan(session)

    print("\n----------------------------\n")

    # Week 6 — Horizontal IDOR Test
    privilege_results = test_horizontal_privilege_escalation(session)

    print("\n----------------------------\n")

    # Week 6 — Vertical Privilege Escalation
    vertical_results = test_vertical_privilege_escalation(session)

    print("\n----------------------------\n")

    end_time = datetime.now()
    duration = end_time - start_time

    total_vulns = (
        len(sqli_results)
        + len(xss_results)
        + len(privilege_results)
        + len(vertical_results)
        + len(session_results)
    )

    risk_score = calculate_risk_score(
        sqli_results,
        xss_results,
        privilege_results,
        vertical_results,
        session_results
    )

    # Generate Final Report
    generate_report(
        brute_force_all,
        brute_force_results,
        sqli_results,
        xss_results,
        privilege_results,
        vertical_results,
        session_results,
        risk_score,
        total_vulns,
        start_time,
        end_time,
        duration
    )

    print("\n✅ Scan Completed Successfully")


if __name__ == "__main__":
    main()