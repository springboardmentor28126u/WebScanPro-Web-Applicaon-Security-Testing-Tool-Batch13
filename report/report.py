import json
import os
from datetime import datetime

# ── Config ────────────────────────────────────────────────────────────────────

FINDINGS_FILES = {
    "SQL Injection":    "../sql/sqli_findings.json",
    "XSS":              "../xss/xss_findings.json",
    "Authentication":   "../auth/auth_findings.json",
    "Access Control":   "../idor/idor_findings.json",
}

OUTPUT_FILE = "report.html"


# ── Helper: escape HTML special characters ────────────────────────────────────
# Prevents XSS payloads in findings from executing in the browser

def escape(text):
    if not text:
        return "—"
    text = str(text)
    text = text.replace("&",  "&amp;")
    text = text.replace("<",  "&lt;")
    text = text.replace(">",  "&gt;")
    text = text.replace('"',  "&quot;")
    text = text.replace("'",  "&#39;")
    return text


# ── Helper: assign recommendation if not already present ─────────────────────
# xss_findings.json and sqli_findings.json don't save recommendations
# so we assign them here based on the vulnerability type

def get_recommendation(finding, module):

    # if the finding already has a recommendation use it
    if finding.get("recommendation"):
        return finding["recommendation"]
    if finding.get("fix"):
        return finding["fix"]

    # otherwise assign based on module and type
    vuln_type = finding.get("type", "").lower()
    xss_type  = finding.get("xss_type", "").lower()

    # SQL Injection recommendations by type
    if module == "SQL Injection":
        if "error" in vuln_type:
            return "Use parameterized queries. Hide SQL errors from users — never expose raw database error messages."
        elif "union" in vuln_type:
            return "Use parameterized queries / prepared statements. Apply least-privilege to database accounts to limit what data can be fetched."
        elif "boolean" in vuln_type:
            return "Use parameterized queries. Validate and whitelist all user inputs. Use an ORM like SQLAlchemy."
        elif "time" in vuln_type:
            return "Use parameterized queries. Add query timeouts. Monitor for unusually slow database responses."
        else:
            return "Use parameterized queries / prepared statements. Validate all inputs. Use least-privilege database accounts."

    # XSS recommendations by type
    elif module == "XSS":
        if "reflected" in xss_type:
            return "Encode all output before rendering in HTML. Set Content-Security-Policy headers. Never insert user input directly into the page."
        elif "stored" in xss_type:
            return "Sanitize and encode all stored user input before rendering. Use a whitelist of allowed HTML tags. Set HttpOnly cookies."
        elif "dom" in xss_type:
            return "Avoid dangerous JS sinks like document.write(), innerHTML, and eval(). Use textContent instead of innerHTML. Validate URL hash values."
        else:
            return "Encode all output. Set Content-Security-Policy headers. Avoid dangerous JavaScript sinks."

    # default fallback
    else:
        return "Review and fix the identified vulnerability following OWASP guidelines."


# ── Load all findings ─────────────────────────────────────────────────────────

def load_all_findings():
    all_findings = []

    for module, filepath in FINDINGS_FILES.items():
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                data = json.load(f)
                for item in data:
                    item["module"] = module
                all_findings.extend(data)
            print(f"  [+] Loaded {len(data)} findings from {filepath}")
        else:
            print(f"  [-] File not found: {filepath} -- skipping")

    return all_findings


# ── Count severities ──────────────────────────────────────────────────────────

def count_severities(findings):
    counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0, "Info": 0}
    for f in findings:
        sev = f.get("severity", "Info")
        if sev in counts:
            counts[sev] += 1
        else:
            counts["Info"] += 1
    return counts


# ── Severity color mapping ────────────────────────────────────────────────────

def severity_color(severity):
    colors = {
        "Critical": "#E85D75",
        "High":     "#F4A261",
        "Medium":   "#FFD166",
        "Low":      "#3DDC84",
        "Info":     "#6B7AE8",
    }
    return colors.get(severity, "#6B7AE8")


def severity_bg(severity):
    colors = {
        "Critical": "rgba(232, 93, 117, 0.15)",
        "High":     "rgba(244, 162, 97, 0.15)",
        "Medium":   "rgba(255, 209, 102, 0.15)",
        "Low":      "rgba(61, 220, 132, 0.15)",
        "Info":     "rgba(107, 122, 232, 0.15)",
    }
    return colors.get(severity, "rgba(107, 122, 232, 0.15)")


# ── Build the HTML report ─────────────────────────────────────────────────────

def build_html_report(findings):
    severity_counts = count_severities(findings)
    total           = len(findings)
    generated_time  = datetime.now().strftime("%B %d, %Y  %H:%M")

    modules = list(FINDINGS_FILES.keys())

    # ── severity bar chart ────────────────────────────────────────────────────
    max_count  = max(severity_counts.values()) if any(severity_counts.values()) else 1
    chart_bars = ""
    for sev, count in severity_counts.items():
        if count == 0:
            continue
        bar_height = int((count / max_count) * 120)
        color      = severity_color(sev)
        chart_bars += f"""
        <div class="bar-wrap">
            <div class="bar-label-top">{count}</div>
            <div class="bar" style="height:{bar_height}px; background:{color};"></div>
            <div class="bar-label">{sev}</div>
        </div>"""

    # ── summary cards ─────────────────────────────────────────────────────────
    summary_cards = f"""
    <div class="stat-card" style="border-color:#6B7AE8">
        <div class="stat-num" style="color:#6B7AE8">{total}</div>
        <div class="stat-label">Total Issues</div>
    </div>
    <div class="stat-card" style="border-color:#E85D75">
        <div class="stat-num" style="color:#E85D75">{severity_counts['Critical']}</div>
        <div class="stat-label">Critical</div>
    </div>
    <div class="stat-card" style="border-color:#F4A261">
        <div class="stat-num" style="color:#F4A261">{severity_counts['High']}</div>
        <div class="stat-label">High</div>
    </div>
    <div class="stat-card" style="border-color:#FFD166">
        <div class="stat-num" style="color:#FFD166">{severity_counts['Medium']}</div>
        <div class="stat-label">Medium</div>
    </div>
    <div class="stat-card" style="border-color:#3DDC84">
        <div class="stat-num" style="color:#3DDC84">{severity_counts['Low'] + severity_counts['Info']}</div>
        <div class="stat-label">Low / Info</div>
    </div>"""

    # ── findings sections by module ───────────────────────────────────────────
    sections_html = ""

    for module in modules:
        module_findings = [f for f in findings if f.get("module") == module]
        if not module_findings:
            continue

        rows_html = ""
        for i, f in enumerate(module_findings, 1):
            sev      = f.get("severity", "Info")
            color    = severity_color(sev)
            bg       = severity_bg(sev)

            # get recommendation -- auto-assigned if missing
            fix_raw  = get_recommendation(f, module)

            # escape everything before putting into HTML
            test     = escape(f.get("test",     f.get("xss_type", module)))
            endpoint = escape(f.get("endpoint", f.get("page", f.get("url", "—"))))
            evidence = escape(f.get("evidence", "—"))
            fix      = escape(fix_raw)
            payload  = escape(f.get("payload",  ""))

            payload_row = f"""
            <tr>
                <td colspan="4" style="padding:4px 16px 10px 16px; color:#7B84B8; font-size:12px; font-family:monospace; background:#0A0E2A;">
                    Payload: {payload}
                </td>
            </tr>""" if f.get("payload") else ""

            rows_html += f"""
            <tr style="background:{bg}; border-left: 3px solid {color};">
                <td>{i}</td>
                <td>{test}</td>
                <td style="font-family:monospace; font-size:12px;">{endpoint}</td>
                <td><span class="badge" style="background:{color}20; color:{color}; border:1px solid {color};">{sev}</span></td>
            </tr>
            <tr>
                <td colspan="4" style="padding:6px 16px; color:#D8DCF0; font-size:13px;">
                    <strong style="color:#6B7AE8;">Evidence:</strong> {evidence}
                </td>
            </tr>
            <tr>
                <td colspan="4" style="padding:4px 16px 12px 16px; color:#D8DCF0; font-size:13px; border-bottom:1px solid #1E245A;">
                    <strong style="color:#3DDC84;">Fix:</strong> {fix}
                </td>
            </tr>
            {payload_row}"""

        sections_html += f"""
        <div class="section">
            <div class="section-header">
                <span class="section-title">{module}</span>
                <span class="section-count">{len(module_findings)} issue(s)</span>
            </div>
            <table>
                <thead>
                    <tr>
                        <th style="width:40px">#</th>
                        <th>Test / Type</th>
                        <th>Endpoint / Page</th>
                        <th style="width:100px">Severity</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>"""

    # ── mitigations summary ───────────────────────────────────────────────────
    mitigations_html = """
    <div class="section">
        <div class="section-header">
            <span class="section-title">Security Best Practices</span>
        </div>
        <div class="miti-grid">
            <div class="miti-card">
                <div class="miti-title" style="color:#E85D75;">SQL Injection</div>
                <ul>
                    <li>Use parameterized queries / prepared statements</li>
                    <li>Validate and whitelist all user inputs</li>
                    <li>Never expose raw SQL errors to users</li>
                    <li>Use least-privilege database accounts</li>
                    <li>Consider using an ORM (SQLAlchemy, Django ORM)</li>
                </ul>
            </div>
            <div class="miti-card">
                <div class="miti-title" style="color:#F4A261;">XSS</div>
                <ul>
                    <li>Encode all output — convert &lt; &gt; to HTML entities</li>
                    <li>Set Content-Security-Policy headers</li>
                    <li>Never use innerHTML or document.write() with user data</li>
                    <li>Set HttpOnly and Secure flags on cookies</li>
                    <li>Use frameworks that auto-escape output (React, Angular)</li>
                </ul>
            </div>
            <div class="miti-card">
                <div class="miti-title" style="color:#FFD166;">Authentication</div>
                <ul>
                    <li>Change all default credentials immediately</li>
                    <li>Add rate limiting and account lockout after 5 attempts</li>
                    <li>Set HttpOnly, Secure, SameSite flags on session cookies</li>
                    <li>Regenerate session ID after every login</li>
                    <li>Use HTTPS everywhere</li>
                </ul>
            </div>
            <div class="miti-card">
                <div class="miti-title" style="color:#3DDC84;">Access Control</div>
                <ul>
                    <li>Implement Role-Based Access Control (RBAC)</li>
                    <li>Never use direct object IDs in URLs — use tokens</li>
                    <li>Always verify ownership server-side</li>
                    <li>Apply least privilege principle</li>
                    <li>Deny access by default — whitelist allowed actions</li>
                </ul>
            </div>
        </div>
    </div>"""

    # ── full HTML ─────────────────────────────────────────────────────────────
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WebScanPro — Security Report</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background: #0A0E2A;
            color: #D8DCF0;
            font-family: 'Segoe UI', Calibri, sans-serif;
            padding: 40px;
            line-height: 1.6;
        }}
        .header {{
            text-align: center;
            padding: 40px 0 30px 0;
            border-bottom: 2px solid #4F5FD5;
            margin-bottom: 40px;
        }}
        .header h1 {{ font-size: 42px; color: #FFFFFF; letter-spacing: 2px; }}
        .header .subtitle {{ color: #6B7AE8; font-size: 18px; margin-top: 8px; }}
        .header .meta {{ color: #7B84B8; font-size: 13px; margin-top: 6px; }}
        .stats-row {{
            display: flex; gap: 16px; justify-content: center;
            margin-bottom: 40px; flex-wrap: wrap;
        }}
        .stat-card {{
            background: #111536; border: 1.5px solid; border-radius: 8px;
            padding: 20px 30px; text-align: center; min-width: 130px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }}
        .stat-num {{ font-size: 42px; font-weight: bold; }}
        .stat-label {{ font-size: 13px; color: #7B84B8; margin-top: 4px; }}
        .chart-section {{
            background: #111536; border: 1px solid #1E245A; border-radius: 8px;
            padding: 30px; margin-bottom: 40px; text-align: center;
        }}
        .chart-title {{ font-size: 18px; font-weight: bold; color: #FFFFFF; margin-bottom: 24px; }}
        .chart {{ display: flex; align-items: flex-end; justify-content: center; gap: 30px; height: 160px; }}
        .bar-wrap {{ display: flex; flex-direction: column; align-items: center; gap: 6px; }}
        .bar {{ width: 55px; border-radius: 4px 4px 0 0; }}
        .bar-label {{ font-size: 12px; color: #7B84B8; }}
        .bar-label-top {{ font-size: 14px; font-weight: bold; color: #D8DCF0; }}
        .section {{
            background: #111536; border: 1px solid #1E245A; border-radius: 8px;
            margin-bottom: 30px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }}
        .section-header {{
            background: #161B45; padding: 14px 20px;
            display: flex; justify-content: space-between; align-items: center;
            border-bottom: 1px solid #1E245A;
        }}
        .section-title {{ font-size: 16px; font-weight: bold; color: #FFFFFF; }}
        .section-count {{
            background: #4F5FD520; color: #6B7AE8; border: 1px solid #4F5FD5;
            padding: 3px 12px; border-radius: 20px; font-size: 12px;
        }}
        table {{ width: 100%; border-collapse: collapse; }}
        thead tr {{ background: #0D1230; }}
        th {{
            padding: 10px 16px; text-align: left; font-size: 12px;
            color: #6B7AE8; text-transform: uppercase; letter-spacing: 1px;
            border-bottom: 1px solid #1E245A;
        }}
        td {{ padding: 10px 16px; font-size: 13px; color: #D8DCF0; vertical-align: top; }}
        .badge {{ padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: bold; }}
        .miti-grid {{
            display: grid; grid-template-columns: 1fr 1fr;
            gap: 20px; padding: 20px;
        }}
        .miti-card {{
            background: #0D1230; border: 1px solid #1E245A;
            border-radius: 6px; padding: 16px 20px;
        }}
        .miti-title {{ font-size: 14px; font-weight: bold; margin-bottom: 10px; }}
        .miti-card ul {{ padding-left: 18px; }}
        .miti-card li {{ font-size: 12px; color: #D8DCF0; margin-bottom: 5px; }}
        .note-banner {{
            background: rgba(107, 122, 232, 0.1); border: 1px solid #4F5FD5;
            border-radius: 8px; padding: 14px 20px; margin-bottom: 30px;
            font-size: 13px; color: #D8DCF0;
        }}
        .note-banner strong {{ color: #6B7AE8; }}
        .footer {{
            text-align: center; padding: 30px 0 10px 0; color: #7B84B8;
            font-size: 12px; border-top: 1px solid #1E245A; margin-top: 40px;
        }}
    </style>
</head>
<body>

    <div class="header">
        <h1>&#128272; WebScanPro</h1>
        <div class="subtitle">Security Vulnerability Report</div>
        <div class="meta">Target: DVWA (localhost:8080) &nbsp;·&nbsp; Generated: {generated_time} &nbsp;·&nbsp; Security Level: Low</div>
    </div>

    <div class="note-banner">
        <strong>Note:</strong> All vulnerability payloads are HTML-encoded for safe display.
        Characters like &lt; and &gt; are escaped so they appear as plain text and do not execute in the browser.
        This is exactly the mitigation recommended for XSS vulnerabilities.
    </div>

    <div class="stats-row">
        {summary_cards}
    </div>

    <div class="chart-section">
        <div class="chart-title">Vulnerability Severity Distribution</div>
        <div class="chart">
            {chart_bars}
        </div>
    </div>

    {sections_html}

    {mitigations_html}

    <div class="footer">
        WebScanPro &nbsp;·&nbsp; Automated Web Application Security Testing Tool &nbsp;·&nbsp; DVWA Target &nbsp;·&nbsp; {generated_time}
    </div>

</body>
</html>"""

    return html


# ── Save report ───────────────────────────────────────────────────────────────

def save_report(html):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\n  Report saved to {OUTPUT_FILE}")
    print(f"  Open report.html in your browser to view the full report.")


# ── Main ──────────────────────────────────────────────────────────────────────

print("=" * 60)
print("  WebScanPro -- Week 7: Security Report Generator")
print("=" * 60)

print("\n  Loading findings from all modules...")
findings = load_all_findings()

if not findings:
    print("\n  No findings found. Make sure you have run all modules first.")
else:
    print(f"\n  Total findings loaded : {len(findings)}")
    counts = count_severities(findings)
    print(f"  Critical : {counts['Critical']}")
    print(f"  High     : {counts['High']}")
    print(f"  Medium   : {counts['Medium']}")
    print(f"  Low/Info : {counts['Low'] + counts['Info']}")

    print("\n  Building HTML report...")
    html = build_html_report(findings)
    save_report(html)

print("\n" + "=" * 60)
