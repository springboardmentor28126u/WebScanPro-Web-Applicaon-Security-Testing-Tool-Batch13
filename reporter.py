import datetime

# --- SETTING UP THE DATA ---
scan_results = [
    {
        "type": "SQL Injection (Error-Based)",
        "endpoint": "/vulnerabilities/sqli/",
        "severity": "High",
        "description": "The application fails to sanitize input in the 'id' field, allowing direct database queries.",
        "mitigation": "Use Parameterized Queries (Prepared Statements) and input validation."
    },
    {
        "type": "Cross-Site Scripting (Reflected)",
        "endpoint": "/vulnerabilities/xss_r/",
        "severity": "High",
        "description": "JavaScript code injected into the URL is executed by the browser.",
        "mitigation": "Implement Output Encoding and use Content Security Policy (CSP) headers."
    },
    {
        "type": "Broken Authentication",
        "endpoint": "/login.php",
        "severity": "Medium",
        "description": "Application allows weak credentials (admin:password) and lacks lockout mechanisms.",
        "mitigation": "Enforce strong password policies and multi-factor authentication (MFA)."
    },
    {
        "type": "Insecure Session Management",
        "endpoint": "Session Cookies",
        "severity": "Medium",
        "description": "Cookies lack 'HttpOnly' and 'Secure' flags, making them vulnerable to hijacking.",
        "mitigation": "Configure server to send 'Set-Cookie' headers with HttpOnly and Secure attributes."
    },
    {
        "type": "IDOR (Insecure Direct Object Reference)",
        "endpoint": "/vulnerabilities/sqli/?id=",
        "severity": "High",
        "description": "Logged-in users can access other users' private data by changing the 'id' parameter.",
        "mitigation": "Implement Object-Level Access Control checks on the server side."
    }
]

def generate_html_report(findings):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>WebScanPro Security Report</title>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; margin: 40px; background-color: #f4f4f9; }}
            .container {{ background: white; padding: 30px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
            h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background-color: #3498db; color: white; }}
            .badge {{ padding: 5px 10px; border-radius: 4px; color: white; font-size: 0.9em; }}
            .bg-high {{ background-color: #e74c3c; }}
            .bg-medium {{ background-color: #f39c12; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>WebScanPro: Security Assessment Report</h1>
            <p><strong>Scan Date:</strong> {timestamp}</p>
            <p><strong>Target:</strong> Localhost (DVWA)</p>
            <table>
                <thead>
                    <tr>
                        <th>Vulnerability Type</th>
                        <th>Endpoint</th>
                        <th>Severity</th>
                        <th>Mitigation</th>
                    </tr>
                </thead>
                <tbody>
    """

    for issue in findings:
        # Use 'bg-high' for High, 'bg-medium' for everything else
        sev_class = "bg-high" if issue['severity'] == "High" else "bg-medium"
        
        # CORRECTED LINE: Changed issue['fix'] to issue['mitigation']
        html_template += f"""
                    <tr>
                        <td><strong>{issue['type']}</strong><br><small>{issue['description']}</small></td>
                        <td><code>{issue['endpoint']}</code></td>
                        <td><span class="badge {sev_class}">{issue['severity']}</span></td>
                        <td>{issue['mitigation']}</td>
                    </tr>
        """

    html_template += """
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """

    with open("WebScanPro_Final_Report.html", "w") as f:
        f.write(html_template)
    print("\n[+] SUCCESS: Security report generated: WebScanPro_Final_Report.html")

if __name__ == "__main__":
    generate_html_report(scan_results)