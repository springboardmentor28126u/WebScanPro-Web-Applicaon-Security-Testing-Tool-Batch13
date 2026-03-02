import requests
from bs4 import BeautifulSoup
from scanner.config import XSS_PAYLOADS_FILE

def load_payloads(filepath=XSS_PAYLOADS_FILE):
    """Loads XSS payloads from the specified text file."""
    try:
        with open(filepath, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"  [ERROR] Payload file not found: {filepath}")
        return ["<script>alert('XSS')</script>", "<u>XSS_TEST</u>"]

def test_xss(session, url, params, method='GET'):
    """
    Tests a specific URL and its parameters for Reflected XSS.
    Matches the signature used in main.py.
    """
    payloads = load_payloads()
    findings = []
    
    # Standardize method to uppercase
    method = method.upper()

    if not params:
        return findings

    for param in params:
        # Skip common non-injectable or sensitive tokens
        if param.lower() in ['submit', 'login', 'user_token']:
            continue

        for payload in payloads:
            # Prepare test parameters: use '1' for others, payload for the target
            test_params = {p: "Submit" if p.lower() == "submit" else "1" for p in params}
            test_params[param] = payload

            try:
                if method == 'POST':
                    resp = session.post(url, data=test_params, timeout=5)
                else:
                    resp = session.get(url, params=test_params, timeout=5)

                # Check if the exact payload is reflected in the HTML response
                if payload in resp.text:
                    finding = {
                        'url': url,
                        'parameter': param,
                        'payload': payload,
                        'type': 'Cross-Site Scripting (XSS)',
                        'severity': 'HIGH',
                        'method': method,
                        'mitigation': 'Implement context-aware output encoding and use Content Security Policy (CSP).'
                    }
                    findings.append(finding)
                    print(f"  [VULN] XSS detected @ {param} using {method} on {url}")
                    # Move to next parameter once a vulnerability is confirmed to save time
                    break 

            except Exception as e:
                print(f"  [ERROR] Testing XSS on {url}: {e}")

    return findings