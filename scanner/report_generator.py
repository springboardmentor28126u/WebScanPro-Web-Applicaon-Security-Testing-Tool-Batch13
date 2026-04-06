import json
from datetime import datetime
import base64
import io
import matplotlib.pyplot as plt


# ─────────────────────────────────────────────
# 🔥 ENRICHMENT
# ─────────────────────────────────────────────
def enrich_vulnerabilities(raw_data):

    enriched = []

    for i, v in enumerate(raw_data):

        severity = v.get("severity", "Low").capitalize()

        # PARAMETER
        if "parameter" in v:
            parameter = v["parameter"]
        elif "cookie" in v:
            parameter = v["cookie"]
        elif "username" in v:
            parameter = "credentials"
        elif "issue" in v:
            parameter = "session/cookie"
        else:
            parameter = "N/A"

        # PAYLOAD
        if "payload" in v and v["payload"]:
            payload = v["payload"]
        elif "username" in v:
            payload = f"{v.get('username')} / {v.get('password')}"
        elif "issue" in v:
            payload = v["issue"]
        else:
            payload = "N/A"

        # EVIDENCE
        evidence = v.get("evidence", "")
        if "length_difference" in v:
            if evidence:
                evidence += f" | Length Difference: {v['length_difference']}"
            else:
                evidence = f"Length Difference: {v['length_difference']}"

        if not evidence:
            evidence = "Validated via automated testing"

        # MITIGATION
        mitigation = "-"
        if "remediation" in v:
            mitigation = "<br>".join(v["remediation"].values())

        # CVSS
        if "SQL" in v["type"]:
            cvss = 9.0
        elif "XSS" in v["type"]:
            cvss = 7.5
        elif "Brute" in v["type"]:
            cvss = 8.0
        elif "Session" in v["type"]:
            cvss = 6.5
        elif "Cookie" in v["type"]:
            cvss = 5.5
        elif "IDOR" in v["type"]:
            cvss = 7.0
        else:
            cvss = 5.0

        # DESCRIPTION
        desc = "Security issue detected."
        if "SQL" in v["type"]:
            desc = "SQL Injection vulnerability allows database manipulation."
        elif "XSS" in v["type"]:
            desc = "Cross-Site Scripting vulnerability."
        elif "Brute" in v["type"]:
            desc = "Brute force vulnerability."
        elif "Session" in v["type"]:
            desc = "Session handling weakness."
        elif "Cookie" in v["type"]:
            desc = "Cookie security misconfiguration."
        elif "IDOR" in v["type"]:
            desc = "Insecure Direct Object Reference."

        enriched.append({
            "id": f"VULN-{i+1:03}",
            "type": v["type"],
            "endpoint": v.get("url", "-"),
            "parameter": parameter,
            "payload": payload,
            "severity": severity,
            "cvss_score": cvss,
            "description": desc,
            "evidence": evidence,
            "mitigation": mitigation
        })

    return enriched


# ─────────────────────────────────────────────
# 📊 CHARTS (WORKING)
# ─────────────────────────────────────────────
def generate_charts(vulns):

    # PIE
    counts = {"High": 0, "Medium": 0, "Low": 0}
    for v in vulns:
        counts[v["severity"]] += 1

    fig1 = plt.figure()
    plt.pie(counts.values(), labels=counts.keys(), autopct="%1.0f%%")

    buf1 = io.BytesIO()
    plt.savefig(buf1, format="png")
    buf1.seek(0)
    pie = base64.b64encode(buf1.read()).decode()
    plt.close(fig1)

    # BAR
    type_counts = {}
    for v in vulns:
        t = v["type"]
        type_counts[t] = type_counts.get(t, 0) + 1

    fig2 = plt.figure()
    plt.barh(list(type_counts.keys()), list(type_counts.values()))

    buf2 = io.BytesIO()
    plt.savefig(buf2, format="png")
    buf2.seek(0)
    bar = base64.b64encode(buf2.read()).decode()
    plt.close(fig2)

    return pie, bar


# ─────────────────────────────────────────────
# 🌐 FINAL HTML REPORT
# ─────────────────────────────────────────────
def generate_html_report(input_file, output_file="report.html"):

    with open(input_file) as f:
        raw_data = json.load(f)

    all_vulns = []
    for k in raw_data:
        all_vulns.extend(raw_data[k])

    vulns = enrich_vulnerabilities(all_vulns)

    total = len(vulns)
    high = sum(1 for v in vulns if v["severity"] == "High")
    medium = sum(1 for v in vulns if v["severity"] == "Medium")
    low = sum(1 for v in vulns if v["severity"] == "Low")

    pie, bar = generate_charts(vulns)

    html = f"""
    <html>
    <head>
    <style>
    body {{ background:#0d0d1a;color:white;font-family:Segoe UI;padding:30px; }}
    .card {{ background:#12122a;padding:20px;margin:20px 0;border-radius:10px; }}
    .high {{color:red}} .medium{{color:orange}} .low{{color:green}}
    </style>
    </head>

    <body>

    <h1 style="text-align:center;">🔐 Security Report</h1>

    <div class="card">
    Total: {total} | High: {high} | Medium: {medium} | Low: {low}
    </div>

    <div class="card" style="text-align:center;">
        <h2>Visual Analysis</h2>
        <img src="data:image/png;base64,{pie}" width="300">
        <img src="data:image/png;base64,{bar}" width="300">
    </div>
    """

    for v in vulns:
        html += f"""
        <div class="card">
        <b>{v['id']} — {v['type']}</b><br>
        Severity: {v['severity']} | CVSS: {v['cvss_score']}<br>
        Endpoint: {v['endpoint']}<br>
        Parameter: {v['parameter']}<br>
        Payload: {v['payload']}<br>
        Evidence: {v['evidence']}<br>
        Mitigation:<br>{v['mitigation']}
        </div>
        """

    html += "</body></html>"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print("✅ FINAL REPORT WITH CHARTS GENERATED")


# ─────────────────────────────────────────────
# PDF
# ─────────────────────────────────────────────
def generate_pdf(html_file="report.html", output="report.pdf"):
    import pdfkit
    config = pdfkit.configuration(
        wkhtmltopdf=r"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
    )
    pdfkit.from_file(html_file, output, configuration=config)