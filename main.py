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
from utils.request_handler import RequestHandler
from modules.crawler import WebCrawler

def main():
    # Change this if your DVWA URL is different
    base_url = "http://localhost:8080/dvwa"

    print("[*] Web Scan Pro Starting...")

    # Initialize request handler
    request_handler = RequestHandler()

    # Login to DVWA
    if not request_handler.login(base_url):
        print("[-] Login failed. Exiting.")
        return

    print("[+] Login successful!")

    # Start crawler
    crawler = WebCrawler(request_handler.session)
    crawler.crawl(base_url)

    print("[+] Crawling finished.")

if __name__ == "__main__":
    main()
