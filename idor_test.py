import requests
import json

url = "http://localhost/dvwa/vulnerabilities/sqli/"

# Paste your PHPSESSID from browser here
cookies = {
    "PHPSESSID": "17i8d2q3alufh6uvtpo3il3buf",
    "security": "low"
}

test_ids = [1,2,3,4,5]
results = []

for user_id in test_ids:

    params = {
        "id": user_id,
        "Submit": "Submit"
    }

    response = requests.get(url, params=params, cookies=cookies)

    if "First name" in response.text:
        status = "Data Found - Possible IDOR"
    else:
        status = "No Data"

    print(f"ID {user_id}: {status}")

    results.append({
        "tested_id": user_id,
        "result": status
    })

with open("idor_results.json","w") as file:
    json.dump(results,file,indent=4)

print("Scan Completed")