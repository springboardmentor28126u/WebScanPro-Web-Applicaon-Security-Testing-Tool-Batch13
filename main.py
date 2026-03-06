from sqli_tester import run_sqli_scan
from xss_scanner import run_xss_scan

if __name__ == "__main__":
    print("🚀 Starting Web Scan Pro...")

    run_sqli_scan()
    run_xss_scan()

    print("✅ Both Scans Completed Successfully.")