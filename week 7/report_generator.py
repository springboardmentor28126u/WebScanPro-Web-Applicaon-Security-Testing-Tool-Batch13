import matplotlib.pyplot as plt
from collections import Counter

vulnerabilities = [
    {"type": "SQL Injection", "endpoint": "/login", "severity": "High", "mitigation": "Use prepared statements"},
    {"type": "XSS", "endpoint": "/search", "severity": "Medium", "mitigation": "Sanitize user input"},
    {"type": "Weak Authentication", "endpoint": "/admin", "severity": "High", "mitigation": "Enable MFA"},
    {"type": "Missing Security Headers", "endpoint": "Global", "severity": "Low", "mitigation": "Add CSP and HSTS"},
    {"type": "IDOR", "endpoint": "/api/user?id=", "severity": "High", "mitigation": "Implement RBAC"},
]

severity_counts = Counter(v["severity"] for v in vulnerabilities)

labels = list(severity_counts.keys())
values = list(severity_counts.values())

plt.figure()
plt.pie(values, labels=labels, autopct='%1.1f%%')
plt.title("Vulnerability Severity Distribution")

chart_file = "severity_chart.png"
plt.savefig(chart_file)
plt.close()

html_content = f"""
<html>
<head>
<title>Security Vulnerability Dashboard</title>

<style>
body {{
    font-family: 'Segoe UI';
    margin: 0;
    background: #0f172a;
    color: white;
}}

header {{
    background: linear-gradient(90deg,#2563eb,#1e40af);
    padding: 20px;
    text-align: center;
    font-size: 28px;
    font-weight: bold;
}}

.container {{
    padding: 30px;
}}

.cards {{
    display: flex;
    gap: 20px;
    margin-bottom: 30px;
}}

.card {{
    flex: 1;
    padding: 20px;
    border-radius: 10px;
    background: #1e293b;
    text-align: center;
    box-shadow: 0 4px 10px rgba(0,0,0,0.4);
}}

.card h2 {{
    margin: 10px 0;
}}

.chart {{
    background: #1e293b;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 30px;
    text-align: center;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    background: #1e293b;
    border-radius: 10px;
    overflow: hidden;
}}

th {{
    background: #2563eb;
    padding: 15px;
}}

td {{
    padding: 12px;
    border-bottom: 1px solid #334155;
}}

tr:hover {{
    background: #334155;
}}

.high {{
    color: #ef4444;
    font-weight: bold;
}}

.medium {{
    color: #facc15;
    font-weight: bold;
}}

.low {{
    color: #22c55e;
    font-weight: bold;
}}
</style>
</head>

<body>

<header>
Web Application Security Dashboard
</header>

<div class="container">

<div class="cards">
<div class="card">
<h3>Total Issues</h3>
<h2>{len(vulnerabilities)}</h2>
</div>

<div class="card">
<h3>High Risk</h3>
<h2>{severity_counts.get("High",0)}</h2>
</div>

<div class="card">
<h3>Medium Risk</h3>
<h2>{severity_counts.get("Medium",0)}</h2>
</div>

<div class="card">
<h3>Low Risk</h3>
<h2>{severity_counts.get("Low",0)}</h2>
</div>
</div>

<div class="chart">
<h2>Risk Distribution</h2>
<img src="{chart_file}" width="350">
</div>

<h2>Detected Vulnerabilities</h2>

<table>
<tr>
<th>Vulnerability</th>
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
</body>
</html>
"""

with open("vulnerability_dashboard.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Professional report generated!")