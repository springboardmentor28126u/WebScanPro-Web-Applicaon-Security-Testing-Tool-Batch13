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

    key = ("IDOR", "global") if vuln == "IDOR Vulnerability" else (vuln, url)

    if key not in unique:
        unique[key] = True
        filtered_results.append(r)

results = filtered_results

# ---------------- SEVERITY ---------------- #
high = sum(1 for r in results if r.get("severity") == "High")
medium = sum(1 for r in results if r.get("severity") == "Medium")
low = sum(1 for r in results if r.get("severity") == "Low")

# ---------------- SCORE ---------------- #
score = max(0, 100 - (high * 10 + medium * 5 + low * 2))

# ---------------- THREAT LEVEL ---------------- #
if high > 5:
    threat = "CRITICAL"
elif high > 0:
    threat = "ELEVATED"
else:
    threat = "LOW"

# ---------------- OWASP ---------------- #
OWASP_MAP = {
    "SQL Injection": "A03: Injection",
    "XSS": "A03: Injection",
    "Weak Credentials": "A07: Auth Failures",
    "Session Hijacking Risk": "A07: Auth Failures",
    "Cookie Security": "A05: Misconfiguration",
    "IDOR Vulnerability": "A01: Broken Access Control"
}

# ---------------- BUILD CONTENT ---------------- #
rows = ""
details = ""

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

    details += f"""
<div class="finding">
<h3>{i}. {html.escape(vuln)}</h3>
<p><b>Severity:</b> {severity}</p>
<p><b>OWASP:</b> {owasp}</p>
<p><b>URL:</b> {html.escape(r.get("url","N/A"))}</p>
<p><b>Payload:</b> {html.escape(str(r.get("payload","N/A")))}</p>

<p><b>Impact:</b><br>
Attackers may exploit this vulnerability to gain unauthorized access or manipulate data.
</p>

<p><b>Recommendation:</b><br>
{html.escape(r.get("recommendation","Apply secure coding practices"))}
</p>
</div>
"""

scan_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ---------------- HTML ---------------- #
html_page = f"""
<html>
<head>
<title>WebScanPro Report</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<style>
body {{
background: radial-gradient(circle,#020617,#000);
color:#e2e8f0;
font-family:Courier New;
padding:40px;
}}

h1 {{
    text-align: center;
    color: #00f7ff;
    font-size: 48px;              /* 🔥 Bigger size */
    letter-spacing: 2px;          /* cyber spacing */
    margin-bottom: 20px;

    text-shadow: 0 0 4px rgba(0,247,255,0.8),
                 0 0 8px rgba(0,247,255,0.4);
}}


p, td, th {{
text-shadow: none;
}}

.cards {{
display:flex;
gap:20px;
margin:40px 0;
}}

.card {{
flex:1;
background:rgba(255,255,255,0.05);
padding:20px;
border-radius:12px;
text-align:center;
border:1px solid rgba(0,255,255,0.2);
box-shadow: 0 0 10px rgba(0,255,255,0.1);
}}

.card span {{
font-size:30px;
color:#00f7ff;
}}

.chart-box {{
width:250px;
margin:40px auto;
}}

.badge {{
padding:5px 10px;
border-radius:6px;
font-weight:bold;
}}

.high {{background:#ff0033}}
.medium {{background:#ff9800}}
.low {{background:#00ff9c}}

table {{
width:100%;
border-collapse:collapse;
}}

td,th {{
padding:10px;
border-bottom:1px solid #1e293b;
}}

.finding {{
background:rgba(255,255,255,0.05);
padding:20px;
margin-top:20px;
border-left:4px solid #00f7ff;
}}

.score {{
font-size:40px;
text-align:center;
color:#00ff9c;
text-shadow: 0 0 6px rgba(0,255,156,0.6),
             0 0 12px rgba(0,255,156,0.3);
}}
</style>
</head>

<body>

<h1>⚡ WEBSCANPRO SECURITY TESTING TOOL REPORT ⚡</h1>

<p style="text-align:center;">Target: http://localhost/dvwa</p>
<p style="text-align:center;">Scan Time: {scan_date}</p>

<h2 class="score">Security Posture Score: {score}/100</h2>
<h2>Threat Level: <span style="color:red;">{threat}</span></h2>

<div class="cards">
<div class="card">Total<br><span>{len(results)}</span></div>
<div class="card">High<br><span>{high}</span></div>
<div class="card">Medium<br><span>{medium}</span></div>
<div class="card">Low<br><span>{low}</span></div>
</div>

<div class="chart-box">
<canvas id="chart"></canvas>
</div>

<h2>Attack Surface Overview</h2>

<table>
<tr><th>Type</th><th>Severity</th><th>OWASP</th></tr>
{rows}
</table>

<h2>Threat Vectors</h2>
{details}

<h2>Attack Timeline</h2>
<div class="finding">
<p>[+] Scan Started</p>
<p>[!] Vulnerabilities Detected</p>
<p>[!] Exploitable Inputs Found</p>
<p>[+] Scan Completed</p>
</div>

<h2>Risk Analysis</h2>
<div class="finding">
Application contains security flaws that could expose sensitive data.
Immediate fixes recommended.
</div>

<h2>Security Recommendations</h2>
<div class="finding">
<ul>
<li>Use prepared statements</li>
<li>Validate user input</li>
<li>Use strong authentication</li>
<li>Apply access control checks</li>
<li>Secure cookies</li>
</ul>
</div>

<h2>Severity Legend</h2>
<div class="finding">
<p><span class="badge high">High</span> → Critical</p>
<p><span class="badge medium">Medium</span> → Moderate</p>
<p><span class="badge low">Low</span> → Low Risk</p>
</div>

<script>
new Chart(document.getElementById('chart'), {{
type:'doughnut',
data:{{
labels:['High','Medium','Low'],
datasets:[{{
data:[{high},{medium},{low}],
backgroundColor:['#ff0033','#ff9800','#00ff9c']
}}]
}},
options:{{
plugins:{{
legend:{{labels:{{color:'#fff'}}}}
}}
}}
}});
</script>

</body>
</html>
"""

# ---------------- SAVE ---------------- #
file_path = os.path.join(BASE_DIR, "security_report.html")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html_page)

print("🔥 Report Ready:", file_path)
webbrowser.open("file://" + os.path.realpath(file_path))