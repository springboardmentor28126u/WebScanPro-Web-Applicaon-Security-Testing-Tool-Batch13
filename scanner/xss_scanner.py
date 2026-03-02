
from scanner.config import XSS_PAYLOADS_FILE

def clean_url(url):
    return url.split('#')[0]   

def test_xss(session, url, params, method='GET'):
    payloads = open(XSS_PAYLOADS_FILE).read().splitlines()  
    findings = []
    url = clean_url(url)

    
    params = [p for p in params if p is not None]
    if not params: return findings

    for param in params:
        if param.lower() in ['submit', 'login', 'user_token']: continue

        for payload in payloads:
            data = {p: "test" for p in params} 
            data[param] = payload                    
            try:
               
                if method == 'POST':
                    resp = session.post(url, data=data, timeout=5)
                else:
                    resp = session.get(url, params=data, timeout=5)

              
                if payload.lower() in resp.text.lower():
                    findings.append({
                        'url': url, 'parameter': param,
                        'payload': payload, 'type': 'Reflected XSS',
                        'severity': 'HIGH'
                    })
                    print(f"  [VULN] XSS @ {param} -> payload reflected!")
                    break   
            except Exception as e:
                print(f"  Error: {e}")
    return findings