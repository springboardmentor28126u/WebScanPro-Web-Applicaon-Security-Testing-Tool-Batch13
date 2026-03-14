import os

print("Starting Web Vulnerability Scanner...\n")

print("Running Crawler...")
os.system("python crawler.py")

print("\nTesting SQL...")
os.system("python sql_tester.py")

print("\nTesting XSS...")
os.system("python xss_tester.py")

print("\nTesting Brute Force...")
os.system("python bruteforce_testing.py")

print("\nTesting IDOR...")
os.system("python idor_test.py")

print("\nScan Completed. Check results.json files for results.")