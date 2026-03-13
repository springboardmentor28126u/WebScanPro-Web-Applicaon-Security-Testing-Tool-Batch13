import json
import os
import webbrowser
import html
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FILES = [
    os.path.join(BASE_DIR, "..", "Week-3", "sqli_results.json"),
    os.path.join(BASE_DIR, "..", "Week-4", "xss_results.json"),
    os.path.join(BASE_DIR, "..", "Week-5", "auth_results.json"),
    os.path.join(BASE_DIR, "..", "Week-6", "idor_results.json"),
]

results = []

# ---------------- LOAD RESULTS ---------------- #

for file in FILES:

    if not os.path.exists(file):
        continue

    try:

        with open(file, "r", encoding="utf-8") as f:

            data = json.load(f)

            if isinstance(data, dict) and "vulnerabilities" in data:
                results.extend(data["vulnerabilities"])

            elif isinstance(data, list):
                results.extend(data)

            elif isinstance(data, dict):
                results.append(data)

    except:
        continue


# ---------------- REMOVE DUPLICATES ---------------- #

unique = {}
filtered_results = []

for r in results:

    vuln = r.get("type", "Unknown")
    url = r.get("url", "N/A")

    # IDOR may appear multiple times for different IDs
    if vuln == "IDOR Vulnerability":
        key = ("IDOR Vulnerability", "global")
    else:
        key = (vuln, url)

    if key not in unique:
        unique[key] = True
        filtered_results.append(r)

results = filtered_results


# ---------------- SEVERITY COUNTS ---------------- #

high = sum(1 for r in results if r.get("severity") == "High")
medium = sum(1 for r in results if r.get("severity") == "Medium")
low = sum(1 for r in results if r.get("severity") == "Low")


# ---------------- SECURITY SCORE ---------------- #

score = 100 - (high * 10 + medium * 5 + low * 2)

if score < 0:
    score = 0


# ---------------- OWASP MAPPING ---------------- #

OWASP_MAP = {
    "SQL Injection": "A03: Injection",
    "XSS": "A03: Injection",
    "Weak Credentials": "A07: Identification & Authentication Failures",
    "Session Hijacking Risk": "A07: Identification & Authentication Failures",
    "Cookie Security": "A05: Security Misconfiguration",
    "IDOR Vulnerability": "A01: Broken Access Control"
}


# ---------------- BUILD TABLE ---------------- #

rows = ""
details_section = ""

for i, r in enumerate(results, 1):

    vuln = r.get("type", "Unknown")
    severity = r.get("severity", "Low")
    owasp = OWASP_MAP.get(vuln, "Unknown")

    rows += f"""
<tr>
<td>{html.escape(vuln)}</td>
<td><span class="badge {severity.lower()}">{severity}</span></td>
<td>{owasp}</td>
</tr>
"""

    url = r.get("url", "N/A")
    payload = r.get("payload", "N/A")
    recommendation = r.get("recommendation", "Review application security controls")

    details_section += f"""
<div class="finding">

<h3>{i}. {html.escape(vuln)}</h3>

<p><b>Severity:</b> {severity}</p>
<p><b>OWASP Category:</b> {owasp}</p>
<p><b>Affected URL:</b> {html.escape(url)}</p>
<p><b>Payload:</b> {html.escape(str(payload))}</p>

<p><b>Impact:</b><br>
This vulnerability could allow attackers to manipulate application behavior
or access sensitive information.
</p>

<p><b>Recommendation:</b><br>
{html.escape(recommendation)}
</p>

</div>
"""


# ---------------- DATE ---------------- #

scan_date = datetime.now().strftime("%Y-%m-%d")


# ---------------- HTML REPORT ---------------- #

html_page = f"""
<html>

<head>

<title>WebScanPro Security Report</title>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>

<style>

body {{
background:#0f172a;
color:white;
font-family:Arial;
padding:40px;
}}

#report {{
max-width:900px;
margin:auto;
}}

h1,h2 {{
text-align:center;
color:#38bdf8;
}}

.cards {{
display:flex;
gap:20px;
margin:40px 0;
}}

.card {{
flex:1;
background:#1e293b;
padding:20px;
border-radius:10px;
text-align:center;
}}

.card span {{
font-size:28px;
font-weight:bold;
}}

.chart-box {{
width:350px;
margin:40px auto;
}}

table {{
width:100%;
border-collapse:collapse;
background:#1e293b;
}}

th {{
background:#020617;
padding:12px;
}}

td {{
padding:12px;
border-bottom:1px solid #334155;
}}

.badge {{
padding:6px 12px;
border-radius:6px;
font-weight:bold;
}}

.high {{background:#ff4d4d}}
.medium {{background:#ff9800}}
.low {{background:#4caf50}}

.finding {{
background:#1e293b;
padding:20px;
border-radius:10px;
margin-bottom:20px;
}}

button {{
margin-top:40px;
padding:12px 25px;
font-size:16px;
background:#38bdf8;
border:none;
border-radius:6px;
cursor:pointer;
font-weight:bold;
}}

</style>

</head>

<body>

<div id="report">

<h1>🛡 WebScanPro Security Report</h1>

<p style="text-align:center"><b>Target:</b> http://localhost/dvwa</p>
<p style="text-align:center"><b>Scan Date:</b> {scan_date}</p>

<h2>Security Score: {score}/100</h2>

<h2>Executive Summary</h2>

<div class="cards">

<div class="card">
Total Vulnerabilities<br>
<span>{len(results)}</span>
</div>

<div class="card">
High Risk<br>
<span>{high}</span>
</div>

<div class="card">
Medium Risk<br>
<span>{medium}</span>
</div>

<div class="card">
Low Risk<br>
<span>{low}</span>
</div>

</div>

<div class="chart-box">
<canvas id="chart"></canvas>
</div>

<h2>Vulnerability Summary</h2>

<table>

<tr>
<th>Vulnerability</th>
<th>Severity</th>
<th>OWASP Category</th>
</tr>

{rows}

</table>

<h2>Detailed Findings</h2>

{details_section}

</div>

<script>

const ctx = document.getElementById('chart');

const chart = new Chart(ctx,{{
type:'doughnut',
data:{{
labels:['High','Medium','Low'],
datasets:[{{
data:[{high},{medium},{low}],
backgroundColor:['#ff4d4d','#ff9800','#4caf50']
}}]
}}
}});

</script>

</body>
</html>
"""


# ---------------- SAVE REPORT ---------------- #

report_file = os.path.join(BASE_DIR, "security_report.html")

with open(report_file, "w", encoding="utf-8") as f:
    f.write(html_page)

print("Security report generated:", report_file)

webbrowser.open("file://" + os.path.realpath(report_file))