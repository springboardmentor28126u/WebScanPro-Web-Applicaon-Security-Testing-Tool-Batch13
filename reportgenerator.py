#!/usr/bin/env python3
"""
Week 7: Security Report Generator
Generates HTML and PDF vulnerability reports from scan results.
"""

import json
import os
import base64
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import io

# ─────────────────────────────────────────────
# 1. LOAD SCAN DATA
# ─────────────────────────────────────────────
def load_scan_results(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# ─────────────────────────────────────────────
# 2. CHART GENERATION (returns base64 PNG)
# ─────────────────────────────────────────────
SEVERITY_COLORS = {
    'High':   '#e74c3c',
    'Medium': '#f39c12',
    'Low':    '#27ae60'
}

TYPE_COLORS = [
    '#e74c3c','#c0392b','#e67e22','#f39c12',
    '#2ecc71','#27ae60','#3498db','#2980b9',
    '#9b59b6','#8e44ad','#1abc9c','#16a085'
]

def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=130, bbox_inches='tight',
                facecolor='none', transparent=True)
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return encoded

def make_severity_pie(vulns):
    counts = {'High': 0, 'Medium': 0, 'Low': 0}
    for v in vulns:
        counts[v['severity']] += 1

    labels = [f"{k}  ({v})" for k, v in counts.items() if v > 0]
    sizes  = [v for v in counts.values() if v > 0]
    colors = [SEVERITY_COLORS[k] for k, v in counts.items() if v > 0]
    explode = [0.04] * len(sizes)

    fig, ax = plt.subplots(figsize=(5, 4))
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, colors=colors, explode=explode,
        autopct='%1.0f%%', startangle=140,
        textprops={'color': '#ecf0f1', 'fontsize': 11},
        wedgeprops={'edgecolor': '#1a1a2e', 'linewidth': 1.5}
    )
    for at in autotexts:
        at.set_fontsize(10)
        at.set_color('white')
        at.set_fontweight('bold')
    ax.set_title('Vulnerabilities by Severity', color='#ecf0f1',
                 fontsize=13, fontweight='bold', pad=10)
    fig.patch.set_alpha(0)
    return fig_to_base64(fig)

def make_type_bar(vulns):
    type_counts = {}
    for v in vulns:
        t = v['type'].split('(')[0].strip()
        type_counts[t] = type_counts.get(t, 0) + 1

    types  = list(type_counts.keys())
    counts = list(type_counts.values())
    colors = TYPE_COLORS[:len(types)]

    fig, ax = plt.subplots(figsize=(7, 3.8))
    bars = ax.barh(types, counts, color=colors, edgecolor='#1a1a2e',
                   linewidth=0.8, height=0.6)
    for bar, count in zip(bars, counts):
        ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
                str(count), va='center', ha='left',
                color='#ecf0f1', fontsize=10, fontweight='bold')

    ax.set_xlabel('Count', color='#ecf0f1', fontsize=10)
    ax.set_title('Vulnerabilities by Type', color='#ecf0f1',
                 fontsize=13, fontweight='bold', pad=10)
    ax.tick_params(colors='#ecf0f1', labelsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    for spine in ['bottom', 'left']:
        ax.spines[spine].set_color('#4a4a6a')
    ax.set_facecolor('none')
    fig.patch.set_alpha(0)
    ax.set_xlim(0, max(counts) + 1.5)
    plt.tight_layout()
    return fig_to_base64(fig)

def make_cvss_scatter(vulns):
    sev_order = {'High': 3, 'Medium': 2, 'Low': 1}
    x = [v['cvss_score'] for v in vulns]
    y = [sev_order[v['severity']] for v in vulns]
    colors = [SEVERITY_COLORS[v['severity']] for v in vulns]

    fig, ax = plt.subplots(figsize=(7, 3))
    ax.scatter(x, y, c=colors, s=120, edgecolors='white', linewidths=0.8, alpha=0.9, zorder=3)

    ax.set_yticks([1, 2, 3])
    ax.set_yticklabels(['Low', 'Medium', 'High'], color='#ecf0f1', fontsize=10)
    ax.set_xlabel('CVSS Score', color='#ecf0f1', fontsize=10)
    ax.set_title('CVSS Score Distribution', color='#ecf0f1',
                 fontsize=13, fontweight='bold', pad=10)
    ax.tick_params(colors='#ecf0f1')
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0.4, 3.6)
    ax.axvline(x=7.0, color='#e74c3c', linestyle='--', alpha=0.4, linewidth=1)
    ax.axvline(x=4.0, color='#f39c12', linestyle='--', alpha=0.4, linewidth=1)
    ax.grid(axis='x', color='#4a4a6a', alpha=0.3)

    patches = [mpatches.Patch(color=c, label=l)
               for l, c in SEVERITY_COLORS.items()]
    ax.legend(handles=patches, loc='lower right',
              labelcolor='#ecf0f1', facecolor='#1a1a2e',
              edgecolor='#4a4a6a', fontsize=9)

    ax.set_facecolor('none')
    fig.patch.set_alpha(0)
    plt.tight_layout()
    return fig_to_base64(fig)

# ─────────────────────────────────────────────
# 3. STATS
# ─────────────────────────────────────────────
def compute_stats(vulns):
    sev_count = {'High': 0, 'Medium': 0, 'Low': 0}
    for v in vulns:
        sev_count[v['severity']] += 1
    avg_cvss = sum(v['cvss_score'] for v in vulns) / len(vulns)
    type_set = set(v['type'].split('(')[0].strip() for v in vulns)
    return sev_count, round(avg_cvss, 2), len(type_set)

# ─────────────────────────────────────────────
# 4. HTML REPORT
# ─────────────────────────────────────────────
SEVERITY_BADGE = {
    'High':   '<span class="badge badge-high">🔴 High</span>',
    'Medium': '<span class="badge badge-medium">🟠 Medium</span>',
    'Low':    '<span class="badge badge-low">🟢 Low</span>'
}

def build_html(data, pie_b64, bar_b64, scatter_b64):
    vulns = data['vulnerabilities']
    info  = data['scan_info']
    sev_count, avg_cvss, type_count = compute_stats(vulns)
    total = len(vulns)
    generated = datetime.now().strftime("%B %d, %Y %H:%M")

    # ── vuln rows ──
    rows = ""
    for v in vulns:
        rows += f"""
        <tr>
          <td><code class="vuln-id">{v['id']}</code></td>
          <td><strong>{v['type']}</strong></td>
          <td><code class="endpoint">{v['endpoint']}</code></td>
          <td>{v['method']}</td>
          <td>{SEVERITY_BADGE[v['severity']]}</td>
          <td><strong>{v['cvss_score']}</strong></td>
        </tr>"""

    # ── detail cards ──
    cards = ""
    for v in vulns:
        sev_cls = v['severity'].lower()
        cards += f"""
        <div class="vuln-card severity-{sev_cls}">
          <div class="card-header">
            <div>
              <span class="vuln-id-tag">{v['id']}</span>
              <span class="vuln-type">{v['type']}</span>
            </div>
            <div class="card-meta">
              {SEVERITY_BADGE[v['severity']]}
              <span class="cvss-chip">CVSS {v['cvss_score']}</span>
            </div>
          </div>
          <div class="card-body">
            <div class="detail-row">
              <span class="detail-label">📍 Endpoint</span>
              <code class="endpoint">{v['endpoint']}</code>
            </div>
            <div class="detail-row">
              <span class="detail-label">🔧 Parameter</span>
              <span>{v['parameter']}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">📝 Description</span>
              <span>{v['description']}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">💉 Payload Used</span>
              <code class="payload">{v['payload']}</code>
            </div>
            <div class="detail-row">
              <span class="detail-label">🔍 Evidence</span>
              <span>{v['evidence']}</span>
            </div>
            <div class="detail-row mitigation">
              <span class="detail-label">🛡️ Mitigation</span>
              <span>{v['mitigation']}</span>
            </div>
          </div>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Security Vulnerability Report — {info['target']}</title>
<style>
  :root {{
    --bg:        #0d0d1a;
    --card-bg:   #12122a;
    --border:    #2a2a4a;
    --accent:    #00d4ff;
    --text:      #e0e0f0;
    --muted:     #8888aa;
    --high:      #e74c3c;
    --medium:    #f39c12;
    --low:       #27ae60;
    --code-bg:   #1a1a35;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: 'Segoe UI', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    padding: 40px 30px;
    line-height: 1.6;
  }}

  /* ── HEADER ── */
  .report-header {{
    text-align: center;
    padding: 50px 20px 40px;
    border-bottom: 2px solid var(--border);
    margin-bottom: 40px;
    position: relative;
  }}
  .report-header::before {{
    content: '';
    position: absolute;
    top: 0; left: 50%;
    transform: translateX(-50%);
    width: 120px; height: 3px;
    background: linear-gradient(90deg, transparent, var(--accent), transparent);
  }}
  .report-title {{
    font-size: 2.4rem;
    font-weight: 800;
    letter-spacing: 2px;
    background: linear-gradient(135deg, #00d4ff, #a855f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 8px;
  }}
  .report-subtitle {{
    color: var(--muted);
    font-size: 1rem;
    margin-bottom: 20px;
  }}
  .meta-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 12px;
    max-width: 700px;
    margin: 20px auto 0;
  }}
  .meta-item {{
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 0.85rem;
  }}
  .meta-item .label {{ color: var(--muted); font-size: 0.75rem; margin-bottom: 2px; }}
  .meta-item .value {{ color: var(--accent); font-weight: 600; }}

  /* ── SECTION TITLE ── */
  h2 {{
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--accent);
    margin: 40px 0 20px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border);
    letter-spacing: 1px;
    text-transform: uppercase;
  }}

  /* ── STAT CARDS ── */
  .stat-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 16px;
    margin-bottom: 40px;
  }}
  .stat-card {{
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 22px 16px;
    text-align: center;
    position: relative;
    overflow: hidden;
  }}
  .stat-card::after {{
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0; height: 3px;
  }}
  .stat-total::after  {{ background: var(--accent); }}
  .stat-high::after   {{ background: var(--high); }}
  .stat-medium::after {{ background: var(--medium); }}
  .stat-low::after    {{ background: var(--low); }}
  .stat-cvss::after   {{ background: #a855f7; }}
  .stat-types::after  {{ background: #3498db; }}
  .stat-number {{
    font-size: 2.4rem;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 6px;
  }}
  .stat-total  .stat-number {{ color: var(--accent); }}
  .stat-high   .stat-number {{ color: var(--high); }}
  .stat-medium .stat-number {{ color: var(--medium); }}
  .stat-low    .stat-number {{ color: var(--low); }}
  .stat-cvss   .stat-number {{ color: #a855f7; }}
  .stat-types  .stat-number {{ color: #3498db; }}
  .stat-label {{ font-size: 0.8rem; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; }}

  /* ── CHARTS ── */
  .chart-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-bottom: 20px;
  }}
  .chart-grid-3 {{
    display: grid;
    grid-template-columns: 1fr;
    gap: 20px;
    margin-bottom: 40px;
  }}
  .chart-box {{
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
  }}
  .chart-box img {{ max-width: 100%; height: auto; border-radius: 6px; }}

  /* ── TABLE ── */
  .table-wrap {{ overflow-x: auto; margin-bottom: 40px; }}
  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.88rem;
  }}
  thead tr {{
    background: linear-gradient(90deg, #1a1a35, #12122a);
    border-bottom: 2px solid var(--accent);
  }}
  th {{
    padding: 13px 14px;
    text-align: left;
    color: var(--accent);
    font-size: 0.78rem;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    font-weight: 700;
  }}
  tbody tr {{
    border-bottom: 1px solid var(--border);
    transition: background 0.15s;
  }}
  tbody tr:hover {{ background: rgba(0,212,255,0.04); }}
  td {{
    padding: 11px 14px;
    vertical-align: middle;
  }}

  /* ── BADGES ── */
  .badge {{
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.5px;
  }}
  .badge-high   {{ background: rgba(231,76,60,0.18);  color: #e74c3c; border: 1px solid #e74c3c; }}
  .badge-medium {{ background: rgba(243,156,18,0.18); color: #f39c12; border: 1px solid #f39c12; }}
  .badge-low    {{ background: rgba(39,174,96,0.18);  color: #27ae60; border: 1px solid #27ae60; }}

  /* ── CODE ── */
  code, .endpoint, .payload {{
    font-family: 'Cascadia Code', 'Fira Code', 'Consolas', monospace;
    font-size: 0.83em;
    background: var(--code-bg);
    padding: 2px 7px;
    border-radius: 4px;
    color: #7dd3fc;
    word-break: break-all;
  }}
  .payload {{ color: #fca5a5; }}
  .vuln-id {{ color: #a78bfa; }}

  /* ── DETAIL CARDS ── */
  .vuln-card {{
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 14px;
    margin-bottom: 22px;
    overflow: hidden;
    position: relative;
  }}
  .severity-high   .card-header {{ border-left: 4px solid var(--high);   }}
  .severity-medium .card-header {{ border-left: 4px solid var(--medium); }}
  .severity-low    .card-header {{ border-left: 4px solid var(--low);    }}
  .card-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 20px;
    background: rgba(255,255,255,0.03);
    flex-wrap: wrap;
    gap: 10px;
    border-bottom: 1px solid var(--border);
  }}
  .vuln-id-tag {{
    font-family: monospace;
    background: rgba(168,85,247,0.15);
    color: #a855f7;
    border: 1px solid #a855f7;
    padding: 2px 9px;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: 700;
    margin-right: 10px;
  }}
  .vuln-type {{ font-weight: 700; font-size: 1rem; }}
  .card-meta {{ display: flex; align-items: center; gap: 10px; }}
  .cvss-chip {{
    background: rgba(168,85,247,0.15);
    color: #c084fc;
    border: 1px solid #a855f7;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 700;
  }}
  .card-body {{ padding: 18px 22px; }}
  .detail-row {{
    display: grid;
    grid-template-columns: 130px 1fr;
    gap: 10px;
    margin-bottom: 12px;
    align-items: start;
  }}
  .detail-label {{
    font-size: 0.8rem;
    color: var(--muted);
    font-weight: 600;
    padding-top: 1px;
  }}
  .mitigation {{ background: rgba(39,174,96,0.06); border-radius: 8px; padding: 12px; margin-top: 6px; }}

  /* ── FOOTER ── */
  footer {{
    text-align: center;
    margin-top: 60px;
    padding-top: 20px;
    border-top: 1px solid var(--border);
    color: var(--muted);
    font-size: 0.82rem;
  }}
  footer strong {{ color: var(--accent); }}

  @media (max-width: 600px) {{
    .chart-grid {{ grid-template-columns: 1fr; }}
    .detail-row {{ grid-template-columns: 1fr; }}
  }}
</style>
</head>
<body>

<!-- ════════ HEADER ════════ -->
<header class="report-header">
  <div class="report-title">🔐 SECURITY VULNERABILITY REPORT</div>
  <div class="report-subtitle">Web Application Penetration Testing — Automated Scan Results</div>
  <div class="meta-grid">
    <div class="meta-item"><div class="label">Target Application</div><div class="value">{info['target']}</div></div>
    <div class="meta-item"><div class="label">Scan Date</div><div class="value">{info['scan_date']}</div></div>
    <div class="meta-item"><div class="label">Scanner</div><div class="value">{info['scanner']}</div></div>
    <div class="meta-item"><div class="label">Generated On</div><div class="value">{generated}</div></div>
    <div class="meta-item"><div class="label">Analyst</div><div class="value">{info['tester']}</div></div>
  </div>
</header>

<!-- ════════ STATS ════════ -->
<h2>📊 Executive Summary</h2>
<div class="stat-grid">
  <div class="stat-card stat-total">
    <div class="stat-number">{total}</div>
    <div class="stat-label">Total Issues</div>
  </div>
  <div class="stat-card stat-high">
    <div class="stat-number">{sev_count['High']}</div>
    <div class="stat-label">High Severity</div>
  </div>
  <div class="stat-card stat-medium">
    <div class="stat-number">{sev_count['Medium']}</div>
    <div class="stat-label">Medium Severity</div>
  </div>
  <div class="stat-card stat-low">
    <div class="stat-number">{sev_count['Low']}</div>
    <div class="stat-label">Low Severity</div>
  </div>
  <div class="stat-card stat-cvss">
    <div class="stat-number">{avg_cvss}</div>
    <div class="stat-label">Avg CVSS Score</div>
  </div>
  <div class="stat-card stat-types">
    <div class="stat-number">{type_count}</div>
    <div class="stat-label">Vuln Categories</div>
  </div>
</div>

<!-- ════════ CHARTS ════════ -->
<h2>📈 Visualization</h2>
<div class="chart-grid">
  <div class="chart-box"><img src="data:image/png;base64,{pie_b64}" alt="Severity Pie Chart"></div>
  <div class="chart-box"><img src="data:image/png;base64,{bar_b64}" alt="Type Bar Chart"></div>
</div>
<div class="chart-grid-3">
  <div class="chart-box"><img src="data:image/png;base64,{scatter_b64}" alt="CVSS Scatter"></div>
</div>

<!-- ════════ SUMMARY TABLE ════════ -->
<h2>📋 Vulnerability Summary Table</h2>
<div class="table-wrap">
  <table>
    <thead>
      <tr>
        <th>ID</th><th>Type</th><th>Endpoint</th>
        <th>Method</th><th>Severity</th><th>CVSS</th>
      </tr>
    </thead>
    <tbody>{rows}</tbody>
  </table>
</div>

<!-- ════════ DETAIL CARDS ════════ -->
<h2>🔍 Detailed Findings</h2>
{cards}

<!-- ════════ FOOTER ════════ -->
<footer>
  <p>Generated by <strong>{info['scanner']}</strong> &nbsp;|&nbsp;
     Target: <strong>{info['target']}</strong> &nbsp;|&nbsp;
     Report Date: <strong>{generated}</strong></p>
  <p style="margin-top:6px;font-size:0.75rem;">
    ⚠️ This report is confidential. For authorized security testing only.
  </p>
</footer>

</body>
</html>"""
    return html

# ─────────────────────────────────────────────
# 5. PDF GENERATION
# ─────────────────────────────────────────────
def build_pdf(vulns, info, output_path):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                     Table, TableStyle, HRFlowable,
                                     KeepTogether)
    from reportlab.lib.enums import TA_CENTER, TA_LEFT

    sev_count, avg_cvss, type_count = compute_stats(vulns)
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                             topMargin=1.5*cm, bottomMargin=1.5*cm,
                             leftMargin=1.8*cm, rightMargin=1.8*cm)

    BG    = colors.HexColor('#0d0d1a')
    CARD  = colors.HexColor('#12122a')
    ACCNT = colors.HexColor('#00d4ff')
    HIGH  = colors.HexColor('#e74c3c')
    MED   = colors.HexColor('#f39c12')
    LOW   = colors.HexColor('#27ae60')
    WHITE = colors.HexColor('#e0e0f0')
    MUTED = colors.HexColor('#8888aa')
    PURPL = colors.HexColor('#a855f7')

    S = getSampleStyleSheet()
    def style(name, parent='Normal', **kw):
        return ParagraphStyle(name, parent=S[parent], **kw)

    title_s  = style('T', 'Title', fontSize=22, textColor=ACCNT,
                     alignment=TA_CENTER, spaceAfter=4,
                     fontName='Helvetica-Bold')
    sub_s    = style('Sub', fontSize=10, textColor=MUTED,
                     alignment=TA_CENTER, spaceAfter=14)
    h2_s     = style('H2', fontSize=12, textColor=ACCNT,
                     fontName='Helvetica-Bold', spaceBefore=18, spaceAfter=8)
    body_s   = style('B', fontSize=8.5, textColor=WHITE, leading=13)
    label_s  = style('L', fontSize=8, textColor=MUTED, leading=11)
    code_s   = style('C', fontSize=8, textColor=colors.HexColor('#7dd3fc'),
                     fontName='Courier', leading=11)

    SEV_CLR = {'High': HIGH, 'Medium': MED, 'Low': LOW}

    story = []

    # ── Title ──
    story += [
        Spacer(1, 0.3*cm),
        Paragraph("SECURITY VULNERABILITY REPORT", title_s),
        Paragraph(f"Target: {info['target']}  |  Date: {info['scan_date']}  |  Analyst: {info['tester']}", sub_s),
        HRFlowable(width='100%', thickness=1.5, color=ACCNT, spaceAfter=14),
    ]

    # ── Stats table ──
    story.append(Paragraph("EXECUTIVE SUMMARY", h2_s))
    stat_data = [
        ['Total Issues', 'High', 'Medium', 'Low', 'Avg CVSS', 'Categories'],
        [str(len(vulns)),
         str(sev_count['High']),
         str(sev_count['Medium']),
         str(sev_count['Low']),
         str(avg_cvss),
         str(type_count)]
    ]
    stat_tbl = Table(stat_data, colWidths=[2.8*cm]*6)
    stat_tbl.setStyle(TableStyle([
        ('BACKGROUND',  (0,0), (-1,0), CARD),
        ('TEXTCOLOR',   (0,0), (-1,0), MUTED),
        ('FONTSIZE',    (0,0), (-1,0), 7),
        ('FONTNAME',    (0,0), (-1,0), 'Helvetica-Bold'),
        ('BACKGROUND',  (0,1), (-1,1), colors.HexColor('#1a1a35')),
        ('TEXTCOLOR',   (0,1), (0,1), ACCNT),
        ('TEXTCOLOR',   (1,1), (1,1), HIGH),
        ('TEXTCOLOR',   (2,1), (2,1), MED),
        ('TEXTCOLOR',   (3,1), (3,1), LOW),
        ('TEXTCOLOR',   (4,1), (4,1), PURPL),
        ('TEXTCOLOR',   (5,1), (5,1), colors.HexColor('#3498db')),
        ('FONTSIZE',    (0,1), (-1,1), 18),
        ('FONTNAME',    (0,1), (-1,1), 'Helvetica-Bold'),
        ('ALIGN',       (0,0), (-1,-1), 'CENTER'),
        ('VALIGN',      (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,0),(-1,-1), [CARD, colors.HexColor('#1a1a35')]),
        ('GRID',        (0,0), (-1,-1), 0.4, colors.HexColor('#2a2a4a')),
        ('ROUNDEDCORNERS', [6]),
        ('TOPPADDING',  (0,0), (-1,-1), 8),
        ('BOTTOMPADDING',(0,0),(-1,-1), 8),
    ]))
    story += [stat_tbl, Spacer(1, 0.5*cm)]

    # ── Summary table ──
    story.append(Paragraph("VULNERABILITY SUMMARY TABLE", h2_s))
    hdr = [Paragraph(h, style('TH', fontSize=7, textColor=ACCNT,
                               fontName='Helvetica-Bold'))
           for h in ['ID', 'Type', 'Endpoint', 'Severity', 'CVSS']]
    rows_data = [hdr]
    for v in vulns:
        sc = SEV_CLR[v['severity']]
        rows_data.append([
            Paragraph(v['id'],       style('ci', fontSize=7.5, textColor=PURPL, fontName='Courier')),
            Paragraph(v['type'],     style('vt', fontSize=7.5, textColor=WHITE)),
            Paragraph(v['endpoint'][:55]+'…' if len(v['endpoint'])>55 else v['endpoint'],
                                     style('ep', fontSize=7, textColor=colors.HexColor('#7dd3fc'), fontName='Courier')),
            Paragraph(v['severity'], style('sv', fontSize=7.5, textColor=sc, fontName='Helvetica-Bold')),
            Paragraph(str(v['cvss_score']), style('cs', fontSize=8, textColor=PURPL, fontName='Helvetica-Bold')),
        ])
    col_w = [2*cm, 3.8*cm, 7.5*cm, 2*cm, 1.7*cm]
    tbl = Table(rows_data, colWidths=col_w, repeatRows=1)
    tbl.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (-1,0), colors.HexColor('#1a1a35')),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#12122a'), colors.HexColor('#0f0f25')]),
        ('GRID',         (0,0), (-1,-1), 0.4, colors.HexColor('#2a2a4a')),
        ('TOPPADDING',   (0,0), (-1,-1), 6),
        ('BOTTOMPADDING',(0,0), (-1,-1), 6),
        ('LEFTPADDING',  (0,0), (-1,-1), 6),
        ('VALIGN',       (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story += [tbl, Spacer(1, 0.6*cm)]

    # ── Detail cards ──
    story.append(Paragraph("DETAILED FINDINGS", h2_s))
    for v in vulns:
        sc = SEV_CLR[v['severity']]
        card_data = [
            [Paragraph(f"<b>{v['id']}</b>", style('cid', fontSize=9, textColor=PURPL, fontName='Helvetica-Bold')),
             Paragraph(f"<b>{v['type']}</b>", style('ctype', fontSize=9, textColor=WHITE, fontName='Helvetica-Bold')),
             Paragraph(f"<b>{v['severity']}</b>  CVSS {v['cvss_score']}",
                       style('csev', fontSize=8.5, textColor=sc, fontName='Helvetica-Bold',
                             alignment=2))],
            [Paragraph('<font color="#8888aa">Endpoint</font>', label_s),
             Paragraph(v['endpoint'], code_s), ''],
            [Paragraph('<font color="#8888aa">Description</font>', label_s),
             Paragraph(v['description'], body_s), ''],
            [Paragraph('<font color="#8888aa">Payload</font>', label_s),
             Paragraph(v['payload'].replace('&','&amp;').replace('<','&lt;').replace('>','&gt;'),
                      style('pl', fontSize=8, textColor=colors.HexColor('#fca5a5'),
                            fontName='Courier', leading=11)), ''],
            [Paragraph('<font color="#8888aa">Mitigation</font>', label_s),
             Paragraph(v['mitigation'], style('mit', fontSize=8.5, textColor=colors.HexColor('#86efac'),
                                               leading=13)), ''],
        ]
        card_tbl = Table(card_data, colWidths=[2.2*cm, 12.5*cm, 3*cm])
        card_tbl.setStyle(TableStyle([
            ('BACKGROUND',  (0,0),(-1,0), colors.HexColor('#1a1a35')),
            ('BACKGROUND',  (0,1),(-1,-1), colors.HexColor('#12122a')),
            ('LINEABOVE',   (0,0),(-1,0), 2, sc),
            ('GRID',        (0,0),(-1,-1), 0.3, colors.HexColor('#2a2a4a')),
            ('TOPPADDING',  (0,0),(-1,-1), 6),
            ('BOTTOMPADDING',(0,0),(-1,-1),6),
            ('LEFTPADDING', (0,0),(-1,-1), 8),
            ('VALIGN',      (0,0),(-1,-1),'TOP'),
            ('SPAN',        (1,1),(2,1)),
            ('SPAN',        (1,2),(2,2)),
            ('SPAN',        (1,3),(2,3)),
            ('SPAN',        (1,4),(2,4)),
        ]))
        story += [KeepTogether([card_tbl, Spacer(1, 0.35*cm)])]

    # ── Footer ──
    story += [
        HRFlowable(width='100%', thickness=0.8, color=colors.HexColor('#2a2a4a'), spaceBefore=20),
        Paragraph(
            f"Generated by {info['scanner']}  |  Confidential — Authorized Security Testing Only",
            style('ft', fontSize=7.5, textColor=MUTED, alignment=TA_CENTER, spaceBefore=8)
        )
    ]

    # background canvas
    def bg(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(BG)
        canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
        canvas.restoreState()

    doc.build(story, onFirstPage=bg, onLaterPages=bg)
    print(f"  PDF saved → {output_path}")

# ─────────────────────────────────────────────
# 6. MAIN
# ─────────────────────────────────────────────
if __name__ == '__main__':
    print("🔐 Security Report Generator — Week 7")
    print("=" * 45)

    data  = load_scan_results('scan_results.json')
    vulns = data['vulnerabilities']
    info  = data['scan_info']

    print(f"  Loaded {len(vulns)} vulnerabilities from scan_results.json")
    print("  Generating charts …")

    pie_b64     = make_severity_pie(vulns)
    bar_b64     = make_type_bar(vulns)
    scatter_b64 = make_cvss_scatter(vulns)

    print("  Building HTML report …")
    html = build_html(data, pie_b64, bar_b64, scatter_b64)
    with open('security_report.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("  HTML saved → security_report.html")

    print("  Building PDF report …")
    build_pdf(vulns, info, 'security_report.pdf')

    print("\n✅ Done!")
    print("   • security_report.html")
    print("   • security_report.pdf")
