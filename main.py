import os

print("=====================================")
print("        WebScanPro Scanner")
print("=====================================\n")

print("Step 1: Running Target Scanner...")
os.system("python crawler.py")

print("\nStep 2: Running SQL Injection Module...")
os.system("python sqli_tester.py")

print("\nStep 3: Running XSS Testing Module...")
os.system("python xss_tester.py")

print("\nStep 4: Generating Final Report...")
os.system("python generate_report.py")

print("\n=====================================")
print("Scan Completed Successfully!")
print("Check output.txt for full report.")
print("=====================================")