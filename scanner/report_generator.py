import json
from datetime import datetime
import pdfkit


def get_severity(vuln_type):
    if "SQLi" in vuln_type:
        return "High"
    if "XSS" in vuln_type:
        return "High"
    if "Brute Force" in vuln_type:
        return "High"
    if "Weak Credentials" in vuln_type:
        return "Medium"
    if "Session" in vuln_type:
        return "Medium"
    if "IDOR" in vuln_type:
        return "High"
    return "Low"


def generate_html_report(input_file, output_file="report.html"):

    with open(input_file, "r") as f:
        data = json.load(f)

    total = 0
    summary = {}

    # Count vulnerabilities
    for category, vulns in data.items():
        summary[category] = len(vulns)
        total += len(vulns)

    html = f"""
    <html>
    <head>
        <title>WebScanPro Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f5f7fa;
                margin: 0;
                padding: 0;
            }}

            .container {{
                width: 90%;
                margin: auto;
                padding: 20px;
            }}

            h1 {{
                text-align: center;
                color: #2c3e50;
            }}

            .card {{
                background: white;
                padding: 20px;
                margin-top: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
            }}

            th, td {{
                padding: 12px;
                border-bottom: 1px solid #ddd;
                text-align: left;
            }}

            th {{
                background-color: #2c3e50;
                color: white;
            }}

            .High {{
                color: #e74c3c;
                font-weight: bold;
            }}

            .Medium {{
                color: #f39c12;
                font-weight: bold;
            }}

            .Low {{
                color: #27ae60;
                font-weight: bold;
            }}

            .summary {{
                display: flex;
                gap: 20px;
                flex-wrap: wrap;
            }}

            .box {{
                flex: 1;
                min-width: 150px;
                background: #3498db;
                color: white;
                padding: 15px;
                border-radius: 8px;
                text-align: center;
            }}
        </style>
    </head>

    <body>
    <div class="container">

    <h1>WebScanPro Security Report</h1>
    <p><b>Date:</b> {datetime.now()}</p>
    """

    # Summary cards
    html += "<div class='card'><h2>Summary</h2><div class='summary'>"

    for k, v in summary.items():
        html += f"<div class='box'>{k.upper()}<br><b>{v}</b></div>"

    html += f"<div class='box'>TOTAL<br><b>{total}</b></div>"
    html += "</div></div>"

    # Table
    html += """
    <div class='card'>
    <h2>Detailed Findings</h2>
    <table>
        <tr>
            <th>Type</th>
            <th>URL</th>
            <th>Parameter</th>
            <th>Payload / Evidence</th>
            <th>Severity</th>
            <th>Mitigation</th>
        </tr>
    """

    for category in data:
        for v in data[category]:

            severity = v.get("severity", get_severity(v["type"]))

            # 🔥 NEW: Extract payload or evidence
            payload = "-"
            if "payload" in v:
                payload = v["payload"]
            elif "true_payload" in v:
                payload = f"TRUE: {v['true_payload']}<br>FALSE: {v['false_payload']}"
            elif "length_difference" in v:
                payload = f"Length diff: {v['length_difference']}"

            # 🔥 NEW: Clean mitigation
            mitigation_data = v.get("remediation", {})
            mitigation = "<br>".join(mitigation_data.values()) if mitigation_data else "-"

            html += f"""
            <tr>
                <td>{v.get("type")}</td>
                <td>{v.get("url", "-")}</td>
                <td>{v.get("parameter", "-")}</td>
                <td>{payload}</td>
                <td class="{severity}">{severity}</td>
                <td>{mitigation}</td>
            </tr>
            """

    html += """
    </table>
    </div>

    </div>
    </body>
    </html>
    """

    with open(output_file, "w") as f:
        f.write(html)

    print(f"[+] HTML report generated: {output_file}")


def generate_pdf(html_file="report.html", output="report.pdf"):
    try:
        config = pdfkit.configuration(
            wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        )
        pdfkit.from_file(html_file, output, configuration=config)
        print(f"[+] PDF report generated: {output}")
    except Exception as e:
        print("[!] PDF generation failed.")
        print("Error:", e)