import json
import os
from scanner.auth import get_session
from scanner.crawler import crawl
from scanner.sqli_scanner import test_sql_injection
from scanner.xss_scanner import test_xss
from scanner.auth_tester import brute_force, check_cookie_security   # Week 5
from scanner.config import TARGET_URL, RESULTS_JSON, LOGIN_URL

def main():
    print("[*] Web Scan Pro Starting...")

    # 1. Session 1 — for crawling (Week 2)
    print("[*] Crawling...")
    session = get_session()
    data = crawl(TARGET_URL, session)

    # Ensure reports folder exists
    os.makedirs(os.path.dirname(RESULTS_JSON), exist_ok=True)
    
    with open(RESULTS_JSON, "w") as f:
        json.dump(data, f, indent=2)
    print(f"[+] Found {len(data)} pages. Metadata saved.")

    # 2. Fresh session — crawling may have hit logout.php (Week 3 & 4)
    print("\n[*] Getting fresh session for testing...")
    session = get_session()

    all_findings = []

    # 3. Combined Testing Loop
    for page in data:
        for form in page.get('forms', []):
            clean_inputs = [i for i in form['inputs'] if i is not None]
            if not clean_inputs:
                continue

            # Testing SQL Injection (Week 3)
            print(f"[*] Testing SQL Injection on: {form['action']}")
            sqli_results = test_sql_injection(session, form['action'], clean_inputs)
            all_findings.extend(sqli_results)

            # Testing XSS (Week 4)
            print(f"[*] Testing XSS on: {form['action']}")
            xss_results = test_xss(
                session, 
                form['action'], 
                clean_inputs, 
                form['method']  # Uses GET or POST based on crawler data
            )
            all_findings.extend(xss_results)

    # 4. Auth & Session Testing (Week 5)
    print("\n[*] Starting Brute Force Test...")
    brute_findings = brute_force(LOGIN_URL, "admin")
    all_findings.extend(brute_findings)

    print("\n[*] Checking Cookie Security...")
    session3 = get_session()
    cookie_findings = check_cookie_security(session3, LOGIN_URL)
    all_findings.extend(cookie_findings)

    # 5. Save Results for Week 7 Report
    print(f"\n[+] Total vulnerabilities found: {len(all_findings)}")
    with open("reports/results.json", "w") as f:
        json.dump(all_findings, f, indent=4)
    
    for f in all_findings:
        print(f"  → [{f['severity']}] {f['type']} @ {f['url']} | param: {f['parameter']}")

if __name__ == "__main__":
    main()