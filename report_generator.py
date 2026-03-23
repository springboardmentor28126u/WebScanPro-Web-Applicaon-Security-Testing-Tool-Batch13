import json
import os
from datetime import datetime
from collections import Counter

RESULTS_FILE = "reports/results.json"
REPORT_FILE  = "reports/security_report.html"

# ── Mitigation suggestions per vulnerability type ─────────────────────────────
MITIGATIONS = {
    "SQL Injection": (
        "Use parameterized queries or prepared statements. "
        "Never concatenate user input directly into SQL queries. "
        "Apply input validation and use an ORM where possible."
    ),
    "Cross-Site Scripting (XSS)": (
        "Implement context-aware output encoding before rendering user input. "
        "Use Content Security Policy (CSP) headers. "
        "Sanitize all input using a trusted library like bleach."
    ),
    "Weak Credentials": (
        "Enforce strong password policy (min 8 chars, mixed case, numbers). "
        "Implement account lockout after 5 failed attempts. "
        "Add CAPTCHA and rate limiting to login forms."
    ),
    "Insecure Cookie": (
        "Set the Secure flag so cookies only travel over HTTPS. "
        "Set the HttpOnly flag to prevent JavaScript from reading cookies. "
        "Set SameSite=Strict to prevent CSRF attacks."
    ),
    "IDOR": (
        "Implement server-side authorization checks on every request. "
        "Never trust user-supplied IDs without verifying ownership. "
        "Use indirect object references or UUIDs instead of sequential IDs."
    ),
    "Path Traversal": (
        "Validate and sanitize all file path inputs. "
        "Use a whitelist of allowed files or directories. "
        "Never pass user input directly to file system operations."
    ),
}

SEVERITY_COLOR = {
    "HIGH":   "#e74c3c",
    "MEDIUM": "#f39c12",
    "LOW":    "#27ae60",
}

# ── Load results ──────────────────────────────────────────────────────────────
def load_results():
    with open(RESULTS_FILE, "r") as f:
        return json.load(f)

# ── Deduplicate: keep unique url+parameter+type combinations ──────────────────
def deduplicate(findings):
    seen = set()
    unique = []
    for f in findings:
        key = (f.get("url",""), f.get("parameter",""), f.get("type",""))
        if key not in seen:
            seen.add(key)
            unique.append(f)
    return unique

# ── Build summary counts ───────────────────────────────────────────────────────
def build_summary(findings):
    by_type     = Counter(f.get("type", "Unknown") for f in findings)
    by_severity = Counter(f.get("severity", "UNKNOWN") for f in findings)
    return by_type, by_severity

# ── Generate HTML ─────────────────────────────────────────────────────────────
def generate_html(findings):
    unique    = deduplicate(findings)
    by_type, by_severity = build_summary(unique)
    total     = len(unique)
    timestamp = datetime.now().strftime("%d %B %Y, %I:%M %p")

    # ── severity badge helper ──
    def badge(sev):
        color = SEVERITY_COLOR.get(sev, "#999")
        return f'<span style="background:{color};color:#fff;padding:3px 10px;border-radius:4px;font-size:12px;font-weight:bold;">{sev}</span>'

    # ── rows per finding ──
    rows = ""
    for i, f in enumerate(unique, 1):
        vuln_type  = f.get("type", "Unknown")
        url        = f.get("url", "-")
        param      = f.get("parameter", "-")
        payload    = f.get("payload", "-")
        severity   = f.get("severity", "-")
        mitigation = f.get("mitigation") or MITIGATIONS.get(vuln_type, "Review and apply security best practices.")
        bg         = "#fff8f8" if severity == "HIGH" else "#fffbf0" if severity == "MEDIUM" else "#f8fff8"

        rows += f"""
        <tr style="background:{bg};">
          <td style="padding:10px 12px;border-bottom:1px solid #eee;font-weight:bold;color:#333;">{i}</td>
          <td style="padding:10px 12px;border-bottom:1px solid #eee;color:#c0392b;font-weight:600;">{vuln_type}</td>
          <td style="padding:10px 12px;border-bottom:1px solid #eee;font-family:monospace;font-size:13px;word-break:break-all;">{url}</td>
          <td style="padding:10px 12px;border-bottom:1px solid #eee;font-family:monospace;color:#2980b9;">{param}</td>
          <td style="padding:10px 12px;border-bottom:1px solid #eee;font-family:monospace;font-size:12px;color:#555;word-break:break-all;">{payload}</td>
          <td style="padding:10px 12px;border-bottom:1px solid #eee;text-align:center;">{badge(severity)}</td>
          <td style="padding:10px 12px;border-bottom:1px solid #eee;font-size:13px;color:#555;">{mitigation}</td>
        </tr>"""

    # ── summary cards ──
    summary_cards = ""
    for vtype, count in by_type.items():
        summary_cards += f"""
        <div style="background:#fff;border:1px solid #ddd;border-radius:8px;padding:16px 20px;min-width:180px;text-align:center;box-shadow:0 2px 6px rgba(0,0,0,0.06);">
          <div style="font-size:28px;font-weight:bold;color:#2c3e50;">{count}</div>
          <div style="font-size:13px;color:#777;margin-top:4px;">{vtype}</div>
        </div>"""

    sev_cards = ""
    for sev in ["HIGH", "MEDIUM", "LOW"]:
        count = by_severity.get(sev, 0)
        color = SEVERITY_COLOR.get(sev, "#999")
        sev_cards += f"""
        <div style="background:{color};border-radius:8px;padding:16px 20px;min-width:130px;text-align:center;color:#fff;">
          <div style="font-size:32px;font-weight:bold;">{count}</div>
          <div style="font-size:13px;margin-top:4px;">{sev}</div>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>WebScan-Pro Security Report</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: Arial, sans-serif; background: #f4f6f9; color: #2c3e50; }}
    a {{ color: #2980b9; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th {{ background: #2c3e50; color: #fff; padding: 11px 12px; text-align: left; font-size: 13px; }}
    tr:hover {{ background: #f0f4ff !important; }}
  </style>
</head>
<body>

<!-- HEADER -->
<div style="background:linear-gradient(135deg,#1a6b8a,#0d4f6e);padding:40px;color:#fff;">
  <div style="max-width:1100px;margin:0 auto;">
    <div style="font-size:13px;opacity:0.7;letter-spacing:2px;text-transform:uppercase;">Internship Project</div>
    <h1 style="font-size:36px;margin:8px 0 4px;">WebScan-Pro</h1>
    <div style="font-size:18px;opacity:0.85;">Automated Web Application Security Report</div>
    <div style="margin-top:16px;font-size:13px;opacity:0.7;">
      Generated: {timestamp} &nbsp;|&nbsp; Target: http://localhost:8081 &nbsp;|&nbsp; Tool: WebScan-Pro
    </div>
  </div>
</div>

<!-- SUMMARY -->
<div style="max-width:1100px;margin:30px auto;padding:0 20px;">

  <h2 style="font-size:20px;margin-bottom:16px;color:#1a6b8a;">Executive Summary</h2>
  <div style="background:#fff;border-radius:10px;padding:20px 24px;box-shadow:0 2px 8px rgba(0,0,0,0.07);margin-bottom:20px;">
    <p style="font-size:14px;line-height:1.7;color:#555;">
      This report presents the findings from an automated security scan conducted on DVWA (Damn Vulnerable Web Application)
      using WebScan-Pro. The tool tested for SQL Injection, Cross-Site Scripting, Brute Force vulnerabilities,
      Insecure Cookie configurations, IDOR, and Path Traversal. All identified vulnerabilities are documented below
      with affected endpoints, payloads used, severity ratings, and recommended mitigations.
    </p>
  </div>

  <!-- Total findings -->
  <div style="background:#1a6b8a;color:#fff;border-radius:10px;padding:20px 28px;margin-bottom:24px;display:flex;align-items:center;gap:20px;">
    <div style="font-size:52px;font-weight:bold;">{total}</div>
    <div>
      <div style="font-size:18px;font-weight:bold;">Total Unique Vulnerabilities Found</div>
      <div style="font-size:13px;opacity:0.8;margin-top:4px;">Across all modules — SQL Injection, XSS, Auth, Cookies, IDOR, Path Traversal</div>
    </div>
  </div>

  <!-- By severity -->
  <div style="display:flex;gap:16px;flex-wrap:wrap;margin-bottom:24px;">
    {sev_cards}
  </div>

  <!-- By type -->
  <div style="display:flex;gap:16px;flex-wrap:wrap;margin-bottom:36px;">
    {summary_cards}
  </div>

  <!-- FINDINGS TABLE -->
  <h2 style="font-size:20px;margin-bottom:16px;color:#1a6b8a;">Detailed Findings</h2>
  <div style="background:#fff;border-radius:10px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.07);margin-bottom:40px;">
    <table>
      <thead>
        <tr>
          <th>#</th>
          <th>Vulnerability Type</th>
          <th>Affected URL</th>
          <th>Parameter</th>
          <th>Payload Used</th>
          <th style="text-align:center;">Severity</th>
          <th>Mitigation</th>
        </tr>
      </thead>
      <tbody>
        {rows}
      </tbody>
    </table>
  </div>

  <!-- FOOTER -->
  <div style="text-align:center;padding:20px;color:#aaa;font-size:12px;border-top:1px solid #eee;">
    WebScan-Pro &nbsp;|&nbsp; Automated Web Application Security Testing Tool &nbsp;|&nbsp; Yamini Gaur &nbsp;|&nbsp; {timestamp}
  </div>

</div>
</body>
</html>"""

    return html

# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("[*] WebScan-Pro Report Generator")
    print(f"    Reading : {RESULTS_FILE}")

    findings = load_results()
    print(f"    Findings loaded : {len(findings)}")

    html = generate_html(findings)

    os.makedirs("reports", exist_ok=True)
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    unique_count = len(deduplicate(findings))
    print(f"    Unique findings : {unique_count}")
    print(f"[+] Report saved to : {REPORT_FILE}")
    print(f"    Open in browser : file:///{os.path.abspath(REPORT_FILE)}")