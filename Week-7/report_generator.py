import json
import os
import webbrowser
import html
from datetime import datetime

# Setup base directory for file pathing
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- CONFIGURATION ---
TARGET_URL = "http://localhost/dvwa" 
scan_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# File paths mapped to project milestones
FILES = [
    os.path.join(BASE_DIR, "..", "Week-3", "sqli_results.json"),
    os.path.join(BASE_DIR, "..", "Week-4", "xss_results.json"),
    os.path.join(BASE_DIR, "..", "Week-5", "auth_results.json"),
    os.path.join(BASE_DIR, "..", "Week-6", "idor_results.json"),
]

# Mapping for Dynamic Impact and OWASP Categories
VULN_INTEL = {
    "SQL Injection": {
        "owasp": "A03:2021-Injection",
        "impact": "High. Attackers can bypass authentication, read sensitive database records, modify data, or gain administrative control over the database server."
    },
    "XSS": {
        "owasp": "A03:2021-Injection",
        "impact": "Medium-High. Attackers can execute malicious scripts in the victim's browser to steal session cookies, deface websites, or redirect users to phishing sites."
    },
    "Cross-Site Scripting (XSS)": {
        "owasp": "A03:2021-Injection",
        "impact": "Medium-High. Attackers can execute malicious scripts in the victim's browser to steal session cookies, deface websites, or redirect users to phishing sites."
    },
    "Broken Authentication": {
        "owasp": "A07:2021-Identification and Authentication Failures",
        "impact": "Critical. Compromised accounts allow attackers to impersonate users, access private data, and perform unauthorized actions as an authenticated user."
    },
    "IDOR": {
        "owasp": "A01:2021-Broken Access Control",
        "impact": "High. Attackers can manipulate parameters (like IDs) to access or modify data belonging to other users without authorization."
    },
    "Insecure Direct Object References (IDOR)": {
        "owasp": "A01:2021-Broken Access Control",
        "impact": "High. Attackers can manipulate parameters to access or modify data belonging to other users."
    }
}

results = []

# ---------------- 1. LOAD RESULTS ---------------- #
for file in FILES:
    if not os.path.exists(file):
        continue
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            extracted = data.get("vulnerabilities", data) if isinstance(data, dict) else data
            if extracted:
                results.extend(extracted if isinstance(extracted, list) else [extracted])
    except:
        continue

# ---------------- 2. REMOVE DUPLICATES ---------------- #
unique = {}
filtered_results = []
for r in results:
    vuln = r.get("type", "Unknown")
    url = r.get("url", r.get("endpoint", "Not Required"))
    key = (vuln, url)
    if key not in unique:
        unique[key] = True
        filtered_results.append(r)
results = filtered_results

# ---------------- 3. SEVERITY DETECTION ---------------- #
high = sum(1 for r in results if str(r.get("severity", "")).strip().capitalize() == "High")
medium = sum(1 for r in results if str(r.get("severity", "")).strip().capitalize() == "Medium")
low = sum(1 for r in results if str(r.get("severity", "")).strip().capitalize() == "Low")

# ---------------- 4. RISK CALCULATION ---------------- #
weighted_sum = (high * 10) + (medium * 5) + (low * 2)
criticality_score = min(100, round((weighted_sum / (len(results) * 10)) * 100)) if results else 0
threat = "CRITICAL" if high > 0 else "ELEVATED" if medium > 0 else "SECURE"
status_color = "#ff0055" if high > 0 else "#00f3ff"

# ---------------- 5. BUILD CONTENT ---------------- #
rows = ""
summary_cards = ""
for i, r in enumerate(results, 1):
    type_key = r.get("type", "Unknown")
    intel = VULN_INTEL.get(type_key, {"owasp": "General Security", "impact": "Potential system compromise."})
    
    vuln = html.escape(str(type_key))
    sev = str(r.get("severity", "Low")).strip().capitalize()
    url = html.escape(str(r.get("url") or r.get("endpoint") or "System Wide"))
    payload = html.escape(str(r.get("payload") or "Not Required "))
    mitigation = html.escape(str(r.get("recommendation") or r.get("mitigation") or "Apply secure coding practices"))

    rows += f"""
    <tr>
        <td><b>{vuln}</b></td>
        <td class="text-{sev.lower()}">{sev}</td>
        <td><code>{url}</code></td>
        <td>{mitigation}</td>
    </tr>"""

    summary_cards += f"""
    <div class="cyber-card {sev.lower()}">
        <div class="card-header"><span>FINDING_0{i}</span> {vuln}</div>
        <div class="card-content">
            <p><b>OWASP:</b> {intel['owasp']}</p>
            <p><b>ENDPOINT:</b> {url}</p>
            <p><b>PAYLOAD:</b> <code>{payload}</code></p>
            <p><b>IMPACT:</b> {intel['impact']}</p>
            <p><b>SUGGESTED MITIGATION:</b> {mitigation}</p>
        </div>
    </div>"""

# ---------------- 6. UI TEMPLATE ---------------- #
html_page = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>WebScanPro Report</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono&display=swap');
        
        :root {{ --cyan: #00f3ff; --magenta: #ff0055; --bg: #050505; --card: #111; }}

        body {{ background: var(--bg); color: #FFFFFF; font-family: 'JetBrains Mono', monospace; margin: 0; padding: 0; display: flex; }}

        .hud-sidebar {{ width: 320px; height: 100vh; background: #0a0a0a; border-right: 1px solid #333; position: fixed; padding: 40px 20px; box-sizing: border-box; text-align: center; }}
        .logo {{ font-family: 'Orbitron', sans-serif; color: var(--cyan); letter-spacing: 5px; border-bottom: 2px solid var(--cyan); padding-bottom: 10px; margin-bottom: 30px; }}
        .risk-gauge {{ width: 150px; height: 150px; border-radius: 50%; border: 4px double {status_color}; margin: 0 auto 20px; display: flex; align-items: center; justify-content: center; flex-direction: column; box-shadow: 0 0 20px {status_color}33; }}
        .risk-gauge b {{ font-size: 32px; color: {status_color}; }}
        .stat-block {{ background: #151515; border: 1px solid #333; padding: 15px; margin-bottom: 10px; border-radius: 4px; }}
        .stat-block span {{ color: var(--cyan); font-weight: bold; font-size: 20px; }}

        .terminal-content {{ margin-left: 320px; padding: 60px; width: 100%; box-sizing: border-box; }}
        h1, h2 {{ font-family: 'Orbitron', sans-serif; text-transform: uppercase; letter-spacing: 3px; color: var(--cyan); }}
        .meta-line {{ border-left: 3px solid var(--magenta); padding-left: 20px; margin-bottom: 50px; color: #888; }}

        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th {{ text-align: left; padding: 15px; border-bottom: 2px solid #333; color: var(--cyan); font-size: 12px; }}
        td {{ padding: 15px; border-bottom: 1px solid #222; font-size: 13px; }}
        .text-high {{ color: var(--magenta); }} .text-medium {{ color: orange; }} .text-low {{ color: #00ffaa; }}

        .cyber-card {{ background: var(--card); border: 1px solid #222; margin-top: 20px; border-radius: 0 15px 0 15px; }}
        .card-header {{ background: #1a1a1a; padding: 15px; font-weight: bold; display: flex; align-items: center; gap: 15px; border-bottom: 1px solid #333; }}
        .card-header span {{ background: var(--magenta); color: #fff; padding: 2px 8px; font-size: 10px; }}
        .card-content {{ padding: 20px; line-height: 1.6; font-size: 14px; }}
        code {{ background: #222; color: var(--cyan); padding: 2px 6px; }}

        .btn-gen {{ width: 100%; padding: 15px; background: transparent; border: 1px solid var(--cyan); color: var(--cyan); font-family: 'Orbitron'; cursor: pointer; transition: 0.3s; margin-top: 20px; }}
        .btn-gen:hover {{ background: var(--cyan); color: #000; box-shadow: 0 0 20px var(--cyan); }}

        @media print {{
            @page {{ size: A4; margin: 5mm; }}
            html, body {{ zoom: 86%; background: #fff !important; color: #000 !important; width: 210mm; height: 297mm; }}
            .hud-sidebar, .btn-gen {{ display: none !important; }}
            .terminal-content {{ margin: 0 !important; padding: 10mm !important; width: 100% !important; }}
            .cyber-card, table {{ border: 1px solid #000 !important; background: #fff !important; color: #000 !important; page-break-inside: avoid; }}
            .card-header {{ background: #eee !important; color: #000 !important; border-bottom: 2px solid #000 !important; }}
            h1, h2, th {{ color: #000 !important; }}
            .text-high, .text-medium, .text-low {{ color: #000 !important; font-weight: bold; text-decoration: underline; }}
            .meta-line {{ border-left: 3px solid #000 !important; color: #000 !important; }}
        }}
    </style>
</head>
<body>

<div class="hud-sidebar">
    <div class="logo">WebScanPro</div>
    <div class="risk-gauge">
        <small style="color:#FFFFFF; font-size:12px;">THREAT_LEVEL</small>
        <b>{criticality_score}%</b>
    </div>
    <div style="margin-bottom:30px; color:{status_color}; font-weight:bold;">{threat}_MODE</div>
    <div class="stat-block"><span>{len(results)}</span><br><small>TOTAL VULNERABILITY</small></div>
    <div class="stat-block"><span>{high}</span><br><small>HIGH VULNERABILITY</small></div>
    <div class="stat-block"><span>{medium}</span><br><small>MEDIUM VULNERABILITY</small></div>
    <div class="stat-block"><span>{low}</span><br><small>LOW VULNERABILITY</small></div>
    
    <div style="margin:20px auto; max-width:180px; position: relative;">
        <canvas id="pieChart"></canvas>
    </div>
    
    <button class="btn-gen" onclick="window.print()">GENERATE_PDF</button>
</div>

<div class="terminal-content">
    <h1>WEBSCANPRO WEB SECURITY TESTING TOOL REPORT</h1>
    <div class="meta-line">
        TARGET URL: {TARGET_URL}<br>
        TIMESTAMP: {scan_date}<br>
        AUDIT_STATUS: ANALYSIS_COMPLETE
    </div>

    <h2>VULNERABILITY REPORT</h2>
    <table>
        <thead>
            <tr>
                <th>VULNERABILITY</th>
                <th>SEVERITY</th>
                <th>ENDPOINT</th>
                <th>MITIGATION</th>
            </tr>
        </thead>
        <tbody>{rows}</tbody>
    </table>

    <h2 style="margin-top:60px;">VULNERABILITY SUMMARY</h2>
    {summary_cards}
</div>

<script>
    const ctx = document.getElementById('pieChart').getContext('2d');
    
    new Chart(ctx, {{
        type: 'pie',
        data: {{
            labels: ['High Risk', 'Medium Risk', 'Low Risk'],
            datasets: [{{
                data: [{high}, {medium}, {low}],
                backgroundColor: ['#ff0055', '#ffaa00', '#00ffaa'],
                hoverOffset: 15,
                borderWidth: 2,
                borderColor: '#050505'
            }}]
        }},
        options: {{
            plugins: {{
                legend: {{ display: false }},
                tooltip: {{
                    enabled: true,
                    backgroundColor: 'rgba(10, 10, 10, 0.9)',
                    borderColor: '#00f3ff',
                    borderWidth: 1,
                    titleFont: {{ family: 'Orbitron' }}
                }}
            }}
        }}
    }});
</script>
</body>
</html>
"""

# Save and Launch 
file_path = os.path.join(BASE_DIR, "security_report.html")
with open(file_path, "w", encoding="utf-8") as f:
    f.write(html_page)

print(f"🔥 Security report Generated : {file_path}")
webbrowser.open("file://" + os.path.realpath(file_path))


