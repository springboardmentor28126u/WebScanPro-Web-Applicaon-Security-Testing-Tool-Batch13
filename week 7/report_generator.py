import matplotlib.pyplot as plt
from collections import Counter
import os

# -----------------------------
# Sample vulnerability results
# (Replace with scanner output)
# -----------------------------
vulnerabilities = [
    {"type": "SQL Injection", "endpoint": "/login", "severity": "High", "mitigation": "Use prepared statements"},
    {"type": "XSS", "endpoint": "/search", "severity": "Medium", "mitigation": "Sanitize user input"},
    {"type": "Weak Authentication", "endpoint": "/admin", "severity": "High", "mitigation": "Enable MFA"},
    {"type": "Missing Security Headers", "endpoint": "Global", "severity": "Low", "mitigation": "Add CSP and HSTS"},
    {"type": "IDOR", "endpoint": "/api/user?id=", "severity": "High", "mitigation": "Implement RBAC"},
]

# -----------------------------
# Count severity levels
# -----------------------------
severity_counts = Counter(v["severity"] for v in vulnerabilities)

# -----------------------------
# Generate chart
# -----------------------------
labels = severity_counts.keys()
values = severity_counts.values()

plt.figure()
plt.pie(values, labels=labels, autopct='%1.1f%%')
plt.title("Vulnerability Severity Distribution")

chart_file = "severity_chart.png"
plt.savefig(chart_file)
plt.close()

# -----------------------------
# Generate HTML report
# -----------------------------
html_content = f"""
<!DOCTYPE html>
<html>
<head>
<title>Web Application Security Report</title>

<style>
body {{
    font-family: Arial, sans-serif;
    margin: 0;
    background: #eef2f7;
}}

header {{
    background: linear-gradient(90deg,#2c3e50,#4ca1af);
    color: white;
    padding: 20px;
    text-align: center;
}}

.container {{
    width: 90%;
    margin: auto;
    margin-top: 20px;
}}

.card {{
    background: white;
    padding: 20px;
    margin-bottom: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}}

.dashboard {{
    display: flex;
    gap: 20px;
}}

.stat {{
    flex: 1;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    color: white;
    font-size: 18px;
}}

.highbox {{ background: #e74c3c; }}
.mediumbox {{ background: #f39c12; }}
.lowbox {{ background: #27ae60; }}

table {{
    width: 100%;
    border-collapse: collapse;
}}

th, td {{
    padding: 12px;
    border-bottom: 1px solid #ddd;
}}

th {{
    background: #2c3e50;
    color: white;
}}

.high {{color:red; font-weight:bold;}}
.medium {{color:orange; font-weight:bold;}}
.low {{color:green; font-weight:bold;}}

footer {{
    text-align: center;
    padding: 15px;
    color: gray;
}}
</style>
</head>

<body>

<header>
<h1>Web Application Vulnerability Scanner Report</h1>
<p>Automated Security Assessment Dashboard</p>
</header>

<div class="container">

<div class="card">
<h2>Project Overview</h2>
<p>
This project is a Web Application Vulnerability Scanner designed to identify security weaknesses
in web applications such as SQL Injection, Cross-Site Scripting (XSS), authentication issues,
and configuration errors. The scanner analyzes application endpoints and generates a detailed
security report.
</p>
</div>

<div class="card">
<h2>Why This Project is Important</h2>
<ul>
<li>Helps developers identify security flaws before attackers exploit them.</li>
<li>Improves secure coding practices.</li>
<li>Supports organizations in protecting sensitive user data.</li>
<li>Provides automated security testing.</li>
</ul>
</div>

<div class="card">
<h2>Future Scope</h2>
<ul>
<li>Integration with AI-based vulnerability detection.</li>
<li>Real-time monitoring of web applications.</li>
<li>Automatic patch suggestions.</li>
</ul>
</div>

<div class="card">
<h2>Why Build This Project When Tools Already Exist?</h2>
<p>
Existing tools like OWASP ZAP or commercial scanners are powerful, but building this project helps
students understand how vulnerability detection works internally, including crawling, testing,
and report generation.
</p>
</div>

<div class="card">
<h2>Executive Summary</h2>
<div class="dashboard">
<div class="stat highbox">
High Risk<br>{severity_counts.get("High",0)}
</div>
<div class="stat mediumbox">
Medium Risk<br>{severity_counts.get("Medium",0)}
</div>
<div class="stat lowbox">
Low Risk<br>{severity_counts.get("Low",0)}
</div>
</div>
<p>Total Vulnerabilities Detected: {len(vulnerabilities)}</p>
</div>

<div class="card">
<h2>Severity Distribution</h2>
<center>
<img src="{chart_file}" width="400">
</center>
</div>

<div class="card">
<h2>Detailed Vulnerabilities</h2>
<table>
<tr>
<th>Vulnerability Type</th>
<th>Endpoint</th>
<th>Severity</th>
<th>Mitigation</th>
</tr>
"""

for v in vulnerabilities:
    severity_class = v["severity"].lower()
    html_content += f"""
<tr>
<td>{v['type']}</td>
<td>{v['endpoint']}</td>
<td class="{severity_class}">{v['severity']}</td>
<td>{v['mitigation']}</td>
</tr>
"""

html_content += """
</table>
</div>

<div class="card">
<h2>Common Web Vulnerabilities Explained</h2>
<ul>
<li><b>SQL Injection:</b> Attackers manipulate database queries using malicious input.</li>
<li><b>Cross-Site Scripting (XSS):</b> Injection of malicious scripts into web pages.</li>
<li><b>Weak Authentication:</b> Poor login security allowing unauthorized access.</li>
<li><b>IDOR:</b> Accessing data without proper authorization checks.</li>
</ul>
</div>

</div>

<footer>
Generated by Web Vulnerability Scanner
</footer>

</body>
</html>
"""

# Save report
report_file = "vulnerability_report.html"
with open(report_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print("Report generated:", report_file)