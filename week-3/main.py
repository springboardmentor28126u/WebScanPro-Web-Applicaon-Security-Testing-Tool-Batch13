from scanner.sql_injection import test_url

target = input("Enter target URL with parameter: ")

results = test_url(target)

if results:
    print("Vulnerabilities Found!")
else:
    print("No SQL Injection Detected")
