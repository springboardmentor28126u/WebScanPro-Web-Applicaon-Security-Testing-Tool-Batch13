# main.py
import json
from scanner.auth import get_session
from scanner.crawler import crawl
from scanner.sqli_scanner import test_sql_injection
from scanner.config import TARGET_URL, RESULTS_JSON

# Session 1 — for crawling
print("[*] Crawling...")
session = get_session()
data = crawl(TARGET_URL, session)

with open(RESULTS_JSON, "w") as f:
    json.dump(data, f, indent=2)
print(f"Found {len(data)} pages")

# Fresh session — crawling may have hit logout.php
print("\n[*] Getting fresh session for testing...")
session = get_session()

print("[*] Testing SQL Injection...")
all_findings = []

for page in data:
    for form in page['forms']:
        clean_inputs = [i for i in form['inputs'] if i is not None]
        if clean_inputs:
            all_findings += test_sql_injection(session, form['action'], clean_inputs)

print(f"\nTotal SQL Injection vulnerabilities found: {len(all_findings)}")
for f in all_findings:
    print(f"  → [{f['severity']}] {f['url']} | param: {f['parameter']} | payload: {f['payload']}")

from scanner.xss_scanner import test_xss

print("[*] Testing XSS...")
for page in data:
    for form in page['forms']:
        clean_inputs = [i for i in form['inputs'] if i is not None]
        if clean_inputs:
            all_findings += test_xss(
                session, form['action'], clean_inputs, form['method']
                                     # ↑ pass method so scanner uses GET or POST correctly
            )