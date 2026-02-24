# scanner/sqli_scanner.py
import requests
from scanner.config import SQL_PAYLOADS_FILE

ERROR_SIGNATURES = [
    "you have an error in your sql syntax",
    "warning: mysql",
    "unclosed quotation mark",
    "quoted string not properly terminated",
    "syntax error",
    "mariadb server version",
    "mysql_fetch",
    "supplied argument is not a valid mysql"
]

def load_payloads(filepath=SQL_PAYLOADS_FILE):
    with open(filepath) as f:
        return [line.strip() for line in f if line.strip()]

def clean_url(url):
    return url.split('#')[0]

def test_sql_injection(session, url, params):
    payloads = load_payloads()
    findings = []

    url = clean_url(url)

    # Filter out None/null inputs
    params = [p for p in params if p is not None]

    if not params:
        return findings

    for param in params:
        # Skip non-injectable params
        if param.lower() in ['submit', 'login', 'user_token', 'create_db']:
            continue

        for payload in payloads:
            # Include all params, set Submit if present
            test_params = {p: "Submit" if p.lower() == "submit" else "1" for p in params}
            test_params[param] = payload

            try:
                resp = session.get(url, params=test_params, timeout=5)
                body = resp.text.lower()

                # Debug: print body length so we know we're getting responses
                if len(resp.text) < 10:
                    print(f"  [WARN] Empty response for {url} param={param}")
                    continue

                for sig in ERROR_SIGNATURES:
                    if sig in body:
                        findings.append({
                            'url': url,
                            'parameter': param,
                            'payload': payload,
                            'type': 'SQL Injection',
                            'severity': 'HIGH'
                        })
                        print(f"  [VULN] SQL Injection @ {param} with: {payload}")
                        break

            except Exception as e:
                print(f"  Error: {e}")

    return findings