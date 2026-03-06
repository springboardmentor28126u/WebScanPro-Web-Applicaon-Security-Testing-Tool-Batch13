import crawler
import sql_tester
import xss_tester

def run_scanner():
    target_url = "http://localhost/dvwa"

    print("\nStarting Web Scanner...\n")

    print("Step 1: Crawling the website")
    crawler.crawl(target_url)

    print("Step 2: Testing SQL Injection")
    sql_tester.test_sql_injection(target_url)

    print("Step 3: Testing XSS")
    xss_tester.test_xss(target_url)

    print("\nScan Completed!")

if __name__ == "__main__":
    run_scanner()