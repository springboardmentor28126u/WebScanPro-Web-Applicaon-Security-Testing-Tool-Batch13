import os
import io
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from ai_analyzer import analyze_vulnerability, analyze_full_report


# ── Chart helpers ──────────────────────────────────────────────────────────

PALETTE = {
    "vulnerable": "#E63946",
    "safe":       "#2DC653",
    "Low":        "#F4A261",
    "Medium":     "#F4A261",
    "High":       "#E63946",
    "Critical":   "#9B2226",
    "bg":         "#FAFAF8",
    "text":       "#0D1B2A",
    "grid":       "#D3D1C7",
}


def _fig_to_image(fig, width_cm=16):
    """Convert a matplotlib figure to a ReportLab Image object."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight",
                facecolor=PALETTE["bg"])
    buf.seek(0)
    plt.close(fig)
    w = width_cm * cm
    # keep aspect ratio
    img = Image(buf)
    ratio = img.imageHeight / img.imageWidth
    img.drawWidth  = w
    img.drawHeight = w * ratio
    return img


def _chart_bar(sqli_results, xss_results, brute_force_results,
               privilege_results, session_results, vertical_results):
    """Grouped bar chart — vulnerable vs safe per module."""

    def counts(results, vuln_val):
        v = sum(1 for r in results if r[1] == vuln_val)
        return v, len(results) - v

    sqli_v,  sqli_s  = counts(sqli_results,      "Vulnerable")
    xss_v,   xss_s   = counts(xss_results,        "Reflected")
    brute_v           = (1, 9) if brute_force_results else (0, 10)
    idor_v,  idor_s  = counts(privilege_results,  "Accessible")
    sess_v,  sess_s  = counts(session_results,    "Vulnerable") if session_results else \
                       (sum(1 for r in session_results if r[2] != "None"),
                        sum(1 for r in session_results if r[2] == "None"))
    vert_v,  vert_s  = counts(vertical_results,   "Accessible")

    modules    = ["SQL Injection", "XSS", "Brute Force", "IDOR", "Session", "Vertical Esc."]
    vulnerable = [sqli_v, xss_v, brute_v[0], idor_v,
                  sum(1 for r in session_results if r[2] != "None"),
                  vert_v]
    safe       = [sqli_s, xss_s, brute_v[1], idor_s,
                  sum(1 for r in session_results if r[2] == "None"),
                  vert_s]

    x, w = np.arange(len(modules)), 0.35
    fig, ax = plt.subplots(figsize=(11, 4.5), facecolor=PALETTE["bg"])
    ax.set_facecolor(PALETTE["bg"])

    bv = ax.bar(x - w/2, vulnerable, w, label="Vulnerable",
                color=PALETTE["vulnerable"], zorder=3, linewidth=0)
    bs = ax.bar(x + w/2, safe,       w, label="Safe",
                color=PALETTE["safe"],       zorder=3, linewidth=0)

    for bar in list(bv) + list(bs):
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.05, str(int(h)),
                ha="center", va="bottom", fontsize=8, color=PALETTE["text"])

    ax.set_xticks(x)
    ax.set_xticklabels(modules, fontsize=9, color=PALETTE["text"])
    ax.set_ylabel("Test Cases", fontsize=9, color=PALETTE["text"])
    ax.set_title("Vulnerability Summary — Vulnerable vs Safe per Module",
                 fontsize=11, fontweight="bold", color=PALETTE["text"], pad=10)
    ax.tick_params(colors=PALETTE["text"])
    ax.yaxis.set_tick_params(labelcolor=PALETTE["text"])
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color(PALETTE["grid"])
    ax.yaxis.grid(True, color=PALETTE["grid"], linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)
    ax.legend(fontsize=8, framealpha=0, labelcolor=PALETTE["text"])
    fig.tight_layout()
    return fig


def _chart_pie(sqli_results, xss_results, brute_force_results,
               privilege_results, session_results, vertical_results):
    """Donut chart — severity distribution across all modules."""

    totals = {"Low": 0, "Medium": 0, "High": 0, "Critical": 0}

    for _, _, sev in sqli_results:
        if sev in totals: totals[sev] += 1
    for _, _, sev in xss_results:
        if sev in totals: totals[sev] += 1
    if brute_force_results:
        totals["Critical"] += 1
    for _, _, sev in privilege_results:
        if sev in totals: totals[sev] += 1
    for _, _, sev, _ in session_results:
        if sev in totals: totals[sev] += 1
    for _, _, sev in vertical_results:
        if sev in totals: totals[sev] += 1

    labels = [k for k, v in totals.items() if v > 0]
    sizes  = [totals[k] for k in labels]
    clrs   = [PALETTE[k] for k in labels]

    fig, ax = plt.subplots(figsize=(6, 5), facecolor=PALETTE["bg"])
    ax.set_facecolor(PALETTE["bg"])

    wedges, _, autotexts = ax.pie(
        sizes, labels=None, colors=clrs, autopct="%1.0f%%",
        startangle=140,
        wedgeprops={"linewidth": 2, "edgecolor": PALETTE["bg"]},
        pctdistance=0.78,
    )
    for at in autotexts:
        at.set_fontsize(10)
        at.set_color("white")
        at.set_fontweight("bold")

    ax.add_artist(plt.Circle((0, 0), 0.55, fc=PALETTE["bg"]))
    total = sum(sizes)
    ax.text(0,  0.07, str(total),   ha="center", fontsize=20,
            fontweight="bold", color=PALETTE["text"])
    ax.text(0, -0.13, "findings",   ha="center", fontsize=10,
            color="#5F5E5A")

    patches = [mpatches.Patch(color=PALETTE[l], label=f"{l} ({totals[l]})")
               for l in labels]
    ax.legend(handles=patches, loc="lower center", bbox_to_anchor=(0.5, -0.06),
              ncol=4, fontsize=8, framealpha=0, labelcolor=PALETTE["text"])
    ax.set_title("Severity Distribution — All Modules",
                 fontsize=11, fontweight="bold", color=PALETTE["text"], pad=12)
    fig.tight_layout()
    return fig


def _chart_heatmap(sqli_results, xss_results, brute_force_results,
                   privilege_results, session_results, vertical_results):
    """Heatmap — module × severity."""

    def sev_counts(results, sev_index=2):
        c = {"Low": 0, "Medium": 0, "High": 0, "Very High": 0}
        for r in results:
            s = r[sev_index]
            if s in c: c[s] += 1
        return c

    modules    = ["SQL Injection", "XSS", "Brute Force", "IDOR (H)", "Session", "Vertical Esc."]
    severities = ["Low", "Medium", "High", "Very High"]

    sqli_c = sev_counts(sqli_results)
    xss_c  = sev_counts(xss_results)
    brute_c = {"Low":0,"Medium":0,"High":1,"Very High":1} if brute_force_results \
              else {"Low":0,"Medium":0,"High":0,"Very High":0}
    idor_c  = sev_counts(privilege_results)
    sess_c  = sev_counts(session_results)
    vert_c  = sev_counts(vertical_results)

    matrix = np.array([
        [sqli_c[s] for s in severities],
        [xss_c[s]  for s in severities],
        [brute_c[s] for s in severities],
        [idor_c[s]  for s in severities],
        [sess_c[s]  for s in severities],
        [vert_c[s]  for s in severities],
    ], dtype=float)

    fig, ax = plt.subplots(figsize=(8, 4.5), facecolor=PALETTE["bg"])
    ax.set_facecolor(PALETTE["bg"])

    cmap = LinearSegmentedColormap.from_list(
        "risk", ["#FAFAF8", "#FAC775", "#E63946", "#501313"], N=256
    )
    im = ax.imshow(matrix, cmap=cmap, aspect="auto",
                   vmin=0, vmax=max(matrix.max(), 1))

    for i in range(len(modules)):
        for j in range(len(severities)):
            val = int(matrix[i, j])
            col = "white" if matrix[i, j] > matrix.max() * 0.55 else PALETTE["text"]
            ax.text(j, i, str(val), ha="center", va="center",
                    fontsize=12, fontweight="bold", color=col)

    ax.set_xticks(range(len(severities)))
    ax.set_xticklabels(severities, fontsize=10, color=PALETTE["text"])
    ax.set_yticks(range(len(modules)))
    ax.set_yticklabels(modules, fontsize=9, color=PALETTE["text"])
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    for xv in np.arange(-0.5, len(severities), 1):
        ax.axvline(xv, color=PALETTE["bg"], linewidth=2)
    for yv in np.arange(-0.5, len(modules), 1):
        ax.axhline(yv, color=PALETTE["bg"], linewidth=2)

    cbar = plt.colorbar(im, ax=ax, fraction=0.03, pad=0.04)
    cbar.set_label("Count", fontsize=8, color=PALETTE["text"])
    cbar.ax.tick_params(labelcolor=PALETTE["text"])
    ax.set_title("Risk Heatmap — Module × Severity",
                 fontsize=11, fontweight="bold", color=PALETTE["text"], pad=10)
    fig.tight_layout()
    return fig


# ── Main report function ───────────────────────────────────────────────────

def generate_report(brute_force_all, brute_force_results, sqli_results, xss_results,
                    privilege_results, vertical_results=None, session_results=None,
                    risk_score=None, total_vulns=None,
                    start_time=None, end_time=None, duration=None):

    vertical_results = vertical_results or []
    session_results  = session_results  or []

    pdf_path = os.path.join(os.path.dirname(__file__), "WebScanPro_Report.pdf")

    doc = SimpleDocTemplate(
        pdf_path, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm,  bottomMargin=2*cm
    )

    styles = getSampleStyleSheet()

    # ── Custom styles ──────────────────────────────────────────────
    title_style = ParagraphStyle(
        'Title', parent=styles['Title'],
        fontSize=22, textColor=colors.HexColor("#0D1B2A"), spaceAfter=6
    )
    subtitle_style = ParagraphStyle(
        'Subtitle', parent=styles['Normal'],
        fontSize=10, textColor=colors.HexColor("#0077B6"), spaceAfter=14
    )
    section_style = ParagraphStyle(
        'Section', parent=styles['Normal'],
        fontSize=13, textColor=colors.white,
        backColor=colors.HexColor("#0D1B2A"),
        spaceBefore=14, spaceAfter=8,
        leftIndent=6, rightIndent=6, borderPadding=6
    )
    normal_style = ParagraphStyle(
        'Normal2', parent=styles['Normal'],
        fontSize=10, textColor=colors.HexColor("#1a1a2e"), spaceAfter=4
    )
    mitigation_style = ParagraphStyle(
        'Mitigation', parent=styles['Normal'],
        fontSize=9.5, textColor=colors.HexColor("#1E6B3C"),
        backColor=colors.HexColor("#f0fff4"),
        leftIndent=8, spaceAfter=8, borderPadding=6
    )
    ai_style = ParagraphStyle(
        'AIStyle', parent=styles['Normal'],
        fontSize=9.5, textColor=colors.HexColor("#0D1B2A"),
        backColor=colors.HexColor("#f0f8ff"),
        leftIndent=8, spaceAfter=8, borderPadding=6, leading=16
    )

    # ── Helper functions ───────────────────────────────────────────
    def sp(h=8):
        return Spacer(1, h)

    def section(text):
        return Paragraph(f"  {text}", section_style)

    def info(label, value):
        return Paragraph(f"<b>{label}:</b>  {value}", normal_style)

    def ai_box(analysis):
        formatted = analysis.replace("\n", "<br/>").replace("**", "").replace("* ", "• ")
        return Paragraph(f"<b>OpenRouter API Analysis:</b><br/><br/>{formatted}", ai_style)

    def make_table(headers, rows, col_widths):
        data = [headers] + rows
        t = Table(data, colWidths=col_widths)
        style = [
            ("BACKGROUND",     (0, 0), (-1, 0),  colors.HexColor("#0D1B2A")),
            ("TEXTCOLOR",      (0, 0), (-1, 0),  colors.HexColor("#00B4D8")),
            ("FONTNAME",       (0, 0), (-1, 0),  "Helvetica-Bold"),
            ("FONTSIZE",       (0, 0), (-1, -1), 9),
            ("ALIGN",          (0, 0), (-1, -1), "LEFT"),
            ("VALIGN",         (0, 0), (-1, -1), "MIDDLE"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
            ("GRID",           (0, 0), (-1, -1), 0.4, colors.HexColor("#CCCCCC")),
            ("TOPPADDING",     (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING",  (0, 0), (-1, -1), 5),
            ("LEFTPADDING",    (0, 0), (-1, -1), 6),
        ]
        for r, row in enumerate(rows, 1):
            for c, cell in enumerate(row):
                if cell in ("Vulnerable", "Reflected", "Accessible"):
                    style += [("TEXTCOLOR", (c, r), (c, r), colors.HexColor("#E63946")),
                               ("FONTNAME",  (c, r), (c, r), "Helvetica-Bold")]
                elif cell in ("Safe", "Not Reflected", "Not Found", "Failed",
                              "Blocked", "Adequate length", "Safe — token rotated",
                              "Safe — session invalidated"):
                    style.append(("TEXTCOLOR", (c, r), (c, r), colors.HexColor("#2DC653")))
                elif cell == "High":
                    style += [("TEXTCOLOR", (c, r), (c, r), colors.HexColor("#E63946")),
                               ("FONTNAME",  (c, r), (c, r), "Helvetica-Bold")]
                elif cell == "Medium":
                    style.append(("TEXTCOLOR", (c, r), (c, r), colors.HexColor("#F4A261")))
                elif cell == "Low":
                    style.append(("TEXTCOLOR", (c, r), (c, r), colors.HexColor("#00B4D8")))
                elif cell == "None":
                    style.append(("TEXTCOLOR", (c, r), (c, r), colors.HexColor("#8EAFC2")))
        t.setStyle(TableStyle(style))
        return t

    # ── GET AI ANALYSIS ────────────────────────────────────────────
    print("\n🤖 Getting AI analysis from Openrouter API ...")

    full_ai  = analyze_full_report(sqli_results, xss_results,
                                   brute_force_results, privilege_results)
    sqli_ai  = analyze_vulnerability(
        "SQL Injection",
        "' UNION SELECT username,password FROM users --",
        "Vulnerable", "High", "/dvwa/vulnerabilities/sqli/",
       # max_tokens=150
    )
    xss_ai   = analyze_vulnerability(
        "Cross Site Scripting",
        "<script>alert(document.cookie)</script>",
        "Reflected", "High", "/dvwa/vulnerabilities/xss_r/",
        #max_tokens=150
    )
    brute_ai = analyze_vulnerability(
        "Brute Force", "admin:password",
        "Vulnerable", "High", "/dvwa/vulnerabilities/brute/",
        #max_tokens=150
    )
    idor_ai  = analyze_vulnerability(
        "IDOR", "id=1",
        "Accessible", "Medium", "/dvwa/vulnerabilities/idor/",   # ← FIXED
        #max_tokens=150
    )
    session_ai = analyze_vulnerability(
        "Session Management", "PHPSESSID cookie",
        "Vulnerable", "High", "/dvwa/login.php",
        #max_tokens=150

    )
    vert_ai  = analyze_vulnerability(
        "Vertical Privilege Escalation", "Low-priv session accessing admin pages",
        "Accessible", "High", "/dvwa/security.php",
        #max_tokens=150
    )

    print("✅ AI analysis complete!")

    # ── Build Content ──────────────────────────────────────────────
    content = []
    CW = A4[0] - 4*cm

    # Title
        # ── Title ──────────────────────────────────────────────
    content.append(Paragraph("WebScanPro Security Report", title_style))
    content.append(Paragraph(
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  |  "
        f"Target: http://localhost:8080/dvwa/  |  Tool: WebScanPro v1.0",
        subtitle_style
    ))
    content.append(sp(6))

    # ── Scan Summary ─────────────────────────────
    if start_time:
        content.append(section("Scan Execution Summary"))
        content.append(sp(4))

        content.append(info("Scan Started", str(start_time)))
        content.append(info("Scan Finished", str(end_time)))
        content.append(info("Scan Duration", str(duration)))

        if total_vulns is not None:
            content.append(info("Total Findings", str(total_vulns)))

        if risk_score is not None:
            content.append(info("Overall Risk Score", f"{risk_score} / 10"))

        content.append(sp(10))

    # ── Summary counts ─────────────────────────────────────────────
    vuln_sqli  = sum(1 for _, s, _    in sqli_results      if s == "Vulnerable")
    vuln_xss   = sum(1 for _, s, _    in xss_results       if s == "Reflected")
    vuln_idor  = sum(1 for _, s, _    in privilege_results  if s == "Accessible")
    vuln_vert  = sum(1 for _, s, _    in vertical_results   if s == "Accessible")
    vuln_sess  = sum(1 for _, _, sv, _ in session_results   if sv != "None")
    vuln_brute = 1 if brute_force_results else 0

    summary_data = [
        ["Module", "Affected Endpoint", "Total Tested", "Vulnerable", "Risk Level"],
        ["SQL Injection", "/dvwa/vulnerabilities/sqli/",
         str(len(sqli_results)),
         f"{vuln_sqli} ({round(vuln_sqli/len(sqli_results)*100)}%)" if sqli_results else "0",
         "HIGH"],
        ["XSS", "/dvwa/vulnerabilities/xss_r/",
         str(len(xss_results)),
         f"{vuln_xss} ({round(vuln_xss/len(xss_results)*100)}%)" if xss_results else "0",
         "HIGH"],
        ["Brute Force", "/dvwa/vulnerabilities/brute/",
         "10 pairs", "1 found" if vuln_brute else "0", "CRITICAL"],
        ["IDOR (Horizontal)", "/dvwa/vulnerabilities/idor/",   # ← FIXED endpoint
         str(len(privilege_results)),
         f"{vuln_idor} ({round(vuln_idor/len(privilege_results)*100)}%)" if privilege_results else "0",
         "MEDIUM"],
        ["Session & Cookies", "/dvwa/login.php",
         str(len(session_results)),
         f"{vuln_sess}", "HIGH" if vuln_sess else "NONE"],
        ["Vertical Escalation", "/dvwa/security.php",
         str(len(vertical_results)),
         f"{vuln_vert}", "HIGH" if vuln_vert else "NONE"],
    ]

    content.append(section("Summary — Overall Findings"))
    content.append(sp(4))
    content.append(make_table(
        summary_data[0], summary_data[1:],
        [CW*0.20, CW*0.32, CW*0.13, CW*0.15, CW*0.20]
    ))
    content.append(sp(10))

    # Overall AI
    content.append(section("OpenRouter API — Overall Risk Assessment"))
    content.append(sp(4))
    content.append(ai_box(full_ai))
    content.append(sp(10))

    # ── Section 1: Brute Force ─────────────────────────────────────
    content.append(section("[ 1 ]  Brute Force — Authentication Testing"))
    content.append(sp(4))
    content.append(info("Vulnerability Type", "Weak Credentials / No Account Lockout"))
    content.append(info("Affected Endpoint",  "/dvwa/vulnerabilities/brute/"))
    content.append(info("Affected Parameter", "username, password"))
    content.append(sp(4))

    # Show ALL 10 attempts in the table
    brute_data = [["Attempt", "Username", "Password", "Status", "Severity"]]
    for i, (username, password, status, severity) in enumerate(brute_force_all, 1):
        brute_data.append([
            str(i),
            username,
            password,
            status,
            severity
        ])

    content.append(make_table(
        brute_data[0], brute_data[1:],
        [CW*0.10, CW*0.20, CW*0.20, CW*0.30, CW*0.20]
    ))
    content.append(sp(6))

    # Show finding if credential was found
    if brute_force_results:
        username, password = brute_force_results
        content.append(Paragraph(
            f"Finding: Weak credential found — {username}:{password} "
            f"was accepted by the server.",
            ParagraphStyle(
                'Finding',
                parent=styles['Normal'],
                fontSize=10,
                textColor=colors.HexColor("#E63946"),
                backColor=colors.HexColor("#fff5f5"),
                leftIndent=8,
                spaceAfter=8,
                borderPadding=6
            )
        ))

    content.append(Paragraph(
        "Mitigation: Implement account lockout after 3-5 failed attempts. "
        "Enforce strong password policies. Enable Multi-Factor Authentication (MFA). "
        "Add CAPTCHA to login forms.",
        mitigation_style
    ))
    content.append(ai_box(brute_ai))
    content.append(sp(10))
    # ── Section 2: SQL Injection ───────────────────────────────────
    content.append(section("[ 2 ]  SQL Injection — Database Attack Testing"))
    content.append(sp(4))
    content.append(info("Vulnerability Type", "SQL Injection"))
    content.append(info("Affected Endpoint",  "/dvwa/vulnerabilities/sqli/"))
    content.append(info("Affected Parameter", "id (GET)"))
    content.append(sp(4))

    sqli_rows = [[p, "/dvwa/vulnerabilities/sqli/", "id", s, sv]
                 for p, s, sv in sqli_results]
    content.append(make_table(
        ["Payload", "Affected Endpoint", "Parameter", "Status", "Severity"],
        sqli_rows,
        [CW*0.38, CW*0.30, CW*0.10, CW*0.12, CW*0.10]
    ))
    content.append(sp(6))
    content.append(Paragraph(
        "Mitigation: Use parameterized queries or prepared statements. "
        "Never concatenate user input directly into SQL strings. "
        "Apply input validation and use an ORM where possible.", mitigation_style))
    content.append(ai_box(sqli_ai))
    content.append(sp(10))

    # ── Section 3: XSS ────────────────────────────────────────────
    content.append(section("[ 3 ]  XSS — Cross Site Scripting Testing"))
    content.append(sp(4))
    content.append(info("Vulnerability Type", "Reflected XSS"))
    content.append(info("Affected Endpoint",  "/dvwa/vulnerabilities/xss_r/"))
    content.append(info("Affected Parameter", "name (GET)"))
    content.append(sp(4))

    xss_rows = [[p, "/dvwa/vulnerabilities/xss_r/", "name", s, sv]
                for p, s, sv in xss_results]
    content.append(make_table(
        ["Payload", "Affected Endpoint", "Parameter", "Status", "Severity"],
        xss_rows,
        [CW*0.38, CW*0.30, CW*0.10, CW*0.12, CW*0.10]
    ))
    content.append(sp(6))
    content.append(Paragraph(
        "Mitigation: Encode all output before displaying to the user. "
        "Implement Content Security Policy (CSP) headers. "
        "Sanitize and validate all user inputs on the server side.", mitigation_style))
    content.append(ai_box(xss_ai))
    content.append(sp(10))

    # ── Section 4: IDOR (Horizontal) ──────────────────────────────
    content.append(section("[ 4 ]  IDOR — Horizontal Access Control Testing"))
    content.append(sp(4))
    content.append(info("Vulnerability Type", "Insecure Direct Object Reference (IDOR)"))
    content.append(info("Affected Endpoint",  "/dvwa/vulnerabilities/idor/"))   # ← FIXED
    content.append(info("Affected Parameter", "id (GET)"))
    content.append(sp(4))

    idor_rows = [[f"id={uid}", "/dvwa/vulnerabilities/idor/", "id", s, sv]  # ← FIXED
                 for uid, s, sv in privilege_results]
    content.append(make_table(
        ["ID Tested", "Affected Endpoint", "Parameter", "Status", "Severity"],
        idor_rows,
        [CW*0.18, CW*0.38, CW*0.10, CW*0.18, CW*0.16]
    ))
    content.append(sp(6))
    content.append(Paragraph(
        "Mitigation: Implement Role-Based Access Control (RBAC). "
        "Validate object ownership on every request server-side. "
        "Use indirect reference maps instead of direct database IDs.", mitigation_style))
    content.append(ai_box(idor_ai))
    content.append(sp(10))

    # ── Section 5: Vertical Privilege Escalation ───────────────────
    content.append(section("[ 5 ]  Vertical Privilege Escalation — Admin Page Access"))
    content.append(sp(4))
    content.append(info("Vulnerability Type", "Vertical Privilege Escalation"))
    content.append(info("Affected Endpoint",  "/dvwa/security.php, /dvwa/phpinfo.php"))
    content.append(info("Affected Parameter", "Session Cookie (low-privilege user)"))
    content.append(sp(4))

    if vertical_results:
        vert_rows = [[page, f"/dvwa/{page}", "session", s, sv]
                     for page, s, sv in vertical_results]
    else:
        vert_rows = [["N/A", "N/A", "session", "Not Tested", "None"]]

    content.append(make_table(
        ["Page Tested", "Affected Endpoint", "Parameter", "Status", "Severity"],
        vert_rows,
        [CW*0.20, CW*0.32, CW*0.13, CW*0.20, CW*0.15]
    ))
    content.append(sp(6))
    content.append(Paragraph(
        "Mitigation: Enforce server-side role checks on every admin page. "
        "Never rely on UI hiding alone. Apply RBAC and verify the user's role "
        "on each request before returning sensitive content.", mitigation_style))
    content.append(ai_box(vert_ai))
    content.append(sp(10))

    # ── Section 6: Session & Cookie Testing ───────────────────────
    content.append(section("[ 6 ]  Session & Cookie — Authentication Management Testing"))
    content.append(sp(4))
    content.append(info("Vulnerability Type", "Insecure Session Management"))
    content.append(info("Affected Endpoint",  "/dvwa/login.php"))
    content.append(info("Tests Performed",
                        "Cookie flags, token entropy, session fixation, session invalidation"))
    content.append(sp(4))

    if session_results:
        sess_rows = [[name, test_type, status, severity]
                     for name, status, severity, test_type in session_results]
    else:
        sess_rows = [["N/A", "N/A", "Not Tested", "None"]]

    content.append(make_table(
        ["Cookie / Parameter", "Test Type", "Status", "Severity"],
        sess_rows,
        [CW*0.22, CW*0.22, CW*0.38, CW*0.18]
    ))
    content.append(sp(6))
    content.append(Paragraph(
        "Mitigation: Set HttpOnly and Secure flags on all session cookies. "
        "Regenerate session tokens on login (prevent fixation). "
        "Invalidate server-side sessions on logout. "
        "Use SameSite=Strict to prevent CSRF.", mitigation_style))
    content.append(ai_box(session_ai))
    content.append(sp(10))

    # ── Section 7: Visualizations ──────────────────────────────────
    content.append(section("[ 7 ]  Scan Visualizations"))
    content.append(sp(8))

    content.append(Paragraph("<b>Chart 1 — Vulnerable vs Safe per Module</b>", normal_style))
    content.append(sp(4))
    fig_bar = _chart_bar(sqli_results, xss_results, brute_force_results,
                         privilege_results, session_results, vertical_results)
    content.append(_fig_to_image(fig_bar, width_cm=16))
    content.append(sp(14))

    content.append(Paragraph("<b>Chart 2 — Severity Distribution</b>", normal_style))
    content.append(sp(4))
    fig_pie = _chart_pie(sqli_results, xss_results, brute_force_results,
                         privilege_results, session_results, vertical_results)
    content.append(_fig_to_image(fig_pie, width_cm=10))
    content.append(sp(14))

    content.append(Paragraph("<b>Chart 3 — Risk Heatmap</b>", normal_style))
    content.append(sp(4))
    fig_heat = _chart_heatmap(sqli_results, xss_results, brute_force_results,
                              privilege_results, session_results, vertical_results)
    content.append(_fig_to_image(fig_heat, width_cm=16))
    content.append(sp(14))

    # ── Final Summary Count ────────────────────────────────────────
    content.append(section("Final Summary Count"))
    content.append(sp(4))

    total = vuln_sqli + vuln_xss + vuln_idor + vuln_brute + vuln_sess + vuln_vert

    final_data = [
        ["Module", "Result"],
        ["SQL Injection",
         f"{vuln_sqli} vulnerable payload(s) out of {len(sqli_results)}"],
        ["XSS",
         f"{vuln_xss} reflected payload(s) out of {len(xss_results)}"],
        ["Brute Force",
         "Credential found (admin:password)" if vuln_brute else "No weak credentials found"],
        ["IDOR (Horizontal)",
         f"{vuln_idor} accessible ID(s) out of {len(privilege_results)}"],
        ["Vertical Escalation",
         f"{vuln_vert} admin page(s) accessible out of {len(vertical_results)}"],
        ["Session & Cookies",
         f"{vuln_sess} issue(s) found out of {len(session_results)}"],
        ["Total Findings", str(total)],
    ]

    content.append(make_table(
        final_data[0], final_data[1:],
        [CW*0.3, CW*0.7]
    ))
    content.append(sp(10))
    content.append(Paragraph(
        "This report provides a comprehensive overview of the security assessment performed on the target web application. ",
        ParagraphStyle('Footer', parent=styles['Normal'],
                       fontSize=8, textColor=colors.grey, alignment=1)
    ))

    # ── Build PDF ──────────────────────────────────────────────────
    doc.build(content)
    print(f"\n📄 PDF Report saved: {pdf_path}")
