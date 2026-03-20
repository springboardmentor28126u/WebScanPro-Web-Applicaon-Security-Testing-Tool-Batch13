import requests

# ----------------------------------
# Configuration
# ----------------------------------

BASE_URL = "http://localhost:8080/"
LOGIN_URL = BASE_URL + "login.php"
IDOR_URL = BASE_URL + "vulnerabilities/idor/"

USERNAME = "admin"
PASSWORD = "password"

session = requests.Session()


# ----------------------------------
# Login Function
# ----------------------------------

def login():

    print("\n[+] Logging into DVWA...")

    login_data = {
        "username": USERNAME,
        "password": PASSWORD,
        "Login": "Login"
    }

    response = session.post(LOGIN_URL, data=login_data)

    if response.status_code == 200:
        print("[+] Login Successful")
    else:
        print("[-] Login Failed")


# ----------------------------------
# IDOR Testing Function
# ----------------------------------

def test_idor():

    print("\n[+] Starting IDOR Testing...\n")

    vulnerable_ids = []

    for i in range(1, 10):

        params = {
            "id": i,
            "Submit": "Submit"
        }

        response = session.get(IDOR_URL, params=params)

        print("Testing ID:", i)

        if "User ID" in response.text:
            print("[!] Possible IDOR vulnerability detected for ID:", i)
            vulnerable_ids.append(i)

    return vulnerable_ids


# ----------------------------------
# Privilege Escalation Test
# ----------------------------------

def privilege_test():

    print("\n[+] Testing Privilege Escalation...")

    admin_paths = [
        "admin",
        "admin/dashboard",
        "admin/users"
    ]

    accessible = []

    for path in admin_paths:

        url = BASE_URL + path

        response = session.get(url)

        if response.status_code == 200:
            print("[!] Accessible Admin Path:", url)
            accessible.append(url)

    return accessible


# ----------------------------------
# Report Generation
# ----------------------------------

def generate_report(idor_ids, admin_access):

    print("\n[+] Generating Scan Report...")

    with open("week6_report.txt", "w") as file:

        file.write("WEBSCANPRO - WEEK 6 ACCESS CONTROL REPORT\n")
        file.write("=========================================\n\n")

        file.write("IDOR Testing Results\n")
        file.write("--------------------\n")

        if len(idor_ids) == 0:
            file.write("No IDOR vulnerabilities detected\n")
        else:
            for i in idor_ids:
                file.write(f"Possible IDOR detected using id = {i}\n")

        file.write("\nPrivilege Escalation Results\n")
        file.write("-----------------------------\n")

        if len(admin_access) == 0:
            file.write("No admin endpoints accessible\n")
        else:
            for path in admin_access:
                file.write(f"Accessible admin path: {path}\n")

        file.write("\nRecommendations\n")
        file.write("----------------\n")
        file.write("1. Implement proper authorization checks\n")
        file.write("2. Use Role-Based Access Control (RBAC)\n")
        file.write("3. Avoid exposing sequential object identifiers\n")
        file.write("4. Validate resource ownership before returning data\n")

    print("[+] Report saved as week6_report.txt")


# ----------------------------------
# Main Program
# ----------------------------------

def main():

    print("===================================")
    print(" WebScanPro - Week 6 IDOR Scanner ")
    print("===================================")

    login()

    idor_results = test_idor()

    privilege_results = privilege_test()

    generate_report(idor_results, privilege_results)

    print("\n[+] Scan Completed")


main()