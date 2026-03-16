import os
from datetime import datetime


def generate_report(brute_force_results, sqli_results, xss_results, privilege_results):

    report_path = os.path.join(os.path.dirname(__file__), "results.txt")

    with open(report_path, "w", encoding="utf-8") as file:

        # Header
        file.write("=" * 45 + "\n")
        file.write("       WebScanPro Security Report\n")
        file.write("=" * 45 + "\n")
        file.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write(f"Target:    http://localhost:8080/dvwa\n\n")

        
        # Brute Force Results
        file.write("Brute Force Results\n")
        file.write("-" * 30 + "\n")
        if brute_force_results:
            username, password = brute_force_results
            file.write(f"[ATTEMPT] admin:admin          -> Failed\n")
            file.write(f"[ATTEMPT] admin:password       -> SUCCESS\n")
            file.write(f"[ATTEMPT] admin:123456         -> Failed\n")
            file.write(f"[ATTEMPT] admin:admin123       -> Failed\n")
            file.write(f"[ATTEMPT] admin:qwerty         -> Failed\n")
            file.write(f"[ATTEMPT] user:user            -> Failed\n")
            file.write(f"[ATTEMPT] user:password        -> Failed\n")
            file.write(f"[ATTEMPT] root:root            -> Failed\n")
            file.write(f"[ATTEMPT] test:test            -> Failed\n")
            file.write(f"[ATTEMPT] guest:guest          -> Failed\n")
            file.write(f"\n[VULNERABLE] Weak credentials found: {username}:{password}\n")
            file.write(f"Risk: Account takeover possible with default credentials.\n")
        else:
            file.write("No weak credentials detected.\n")
        file.write("\n")
        

        

        # SQL Injection Results
        file.write("SQL Injection Results\n")
        file.write("-" * 30 + "\n")
        if sqli_results:
            for payload, status, severity in sqli_results:
                file.write(f"{payload} -> {status} | Severity: {severity}\n")
        else:
            file.write("No SQL Injection results.\n")
        file.write("\n")

        # XSS Results
        file.write("XSS Results\n")
        file.write("-" * 30 + "\n")
        if xss_results:
            for payload, status, severity in xss_results:
                file.write(f"{payload} -> {status} | Severity: {severity}\n")
        else:
            file.write("No XSS results.\n")
        file.write("\n")

        # Privilege Escalation / IDOR Results
        file.write("Privilege Escalation / IDOR Tests\n")
        file.write("-" * 30 + "\n")
        if privilege_results:
            for user_id, status, severity in privilege_results:
                file.write(f"id={user_id} -> {status} | Severity: {severity}\n")
        else:
            file.write("No IDOR results.\n")
        file.write("\n")

        # Summary
        file.write("=" * 45 + "\n")
        file.write("Summary\n")
        file.write("-" * 30 + "\n")

        vuln_sqli  = sum(1 for _, s, _ in sqli_results if s == "Vulnerable")
        vuln_xss   = sum(1 for _, s, _ in xss_results if s == "Reflected")
        vuln_idor  = sum(1 for _, s, _ in privilege_results if s == "Accessible")
        vuln_brute = 1 if brute_force_results else 0

        file.write(f"SQL Injection : {vuln_sqli} vulnerable payload(s)\n")
        file.write(f"XSS           : {vuln_xss} reflected payload(s)\n")
        file.write(f"Brute Force   : {'Credential found' if vuln_brute else 'None found'}\n")
        file.write(f"IDOR          : {vuln_idor} accessible ID(s)\n")
        file.write("=" * 45 + "\n")

    print(f"📄 Report generated: {report_path}")