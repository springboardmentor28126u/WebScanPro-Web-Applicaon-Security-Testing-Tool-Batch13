WebScanPro

Automated Web Application Security Testing Tool

1. Project Overview

WebScanPro is a modular web application security testing tool developed to automatically detect SQL Injection and Cross-Site Scripting (XSS) vulnerabilities in web applications.

The tool performs authenticated scanning on intentionally vulnerable applications such as DVWA (Damn Vulnerable Web Application), injects crafted attack payloads into discovered input fields, analyzes server responses for abnormal behavior, classifies vulnerabilities by severity, and generates structured JSON reports.

The system simulates the core behavior of a lightweight automated vulnerability scanner.

2. Project Architecture
WebScanPro/
│
├── crawler/              → Page discovery and metadata extraction
│   └── targets.json      → Discovered forms and input fields
│
├── sql/                  → Advanced SQL Injection testing module
│   └── sqli_findings.json
│
├── xss/                  → XSS testing module
│   └── xss_findings.json
│
├── auth/                 → Authentication handling (session + CSRF)
├── report/               → Structured result handling
├── screenshots/          → Evidence documentation
├── main.py               → Central execution controller
└── README.md

The system follows a modular design:

The crawler discovers targets.

The SQL and XSS modules test discovered inputs.

Each module independently analyzes responses.

Results are stored in structured JSON format.

Milestone 1
Week 1 – Project Initialization and Setup
Implementation

Defined project objectives and vulnerability focus areas.

Deployed DVWA using Docker.

Configured Apache, PHP, and MySQL inside containerized environment.

Set DVWA security level to Low for controlled testing.

Explored:

SQL Injection module

Reflected, Stored, and DOM-based XSS

Authentication and CSRF token handling

Week 2 – Target Scanning Module
Objective

Automatically discover web pages, forms, and input fields.

Implementation

Used requests to send HTTP requests.

Used BeautifulSoup to parse HTML.

Extracted:

Form actions

HTTP methods (GET/POST)

Input field names and types

Filtered and structured targets into targets.json.

Output

The crawler generates structured metadata that is later used by SQL and XSS modules for injection testing.

Milestone 2
Week 3 – SQL Injection Testing Module
Objective

Inject multiple types of SQL payloads and detect vulnerabilities using behavioral analysis.

Supported SQL Injection Techniques

Error-Based SQL Injection

Detects exposed database error messages.

Uses regex-based error signature matching.

Boolean-Based SQL Injection

Injects TRUE and FALSE conditions.

Compares response length differences.

UNION-Based SQL Injection

Attempts to extract database data using UNION SELECT.

Detects abnormal increase in response size.

Time-Based Blind SQL Injection

Uses payloads like SLEEP(3).

Measures response delay.

Detects blind injection without visible output.

Detection Logic

Establish baseline response using safe input.

Inject payload into all text input fields.

Analyze:

SQL error signatures

Response length variation

Response delay timing

Flag vulnerability if anomaly detected.

Assign severity:

Critical → UNION-based

High → Error-based, Time-based

Medium → Boolean-based

Output

Structured vulnerability findings:

{
  "page": "...",
  "endpoint": "...",
  "method": "GET/POST",
  "payload": "...",
  "type": "UNION-Based",
  "evidence": "...",
  "severity": "Critical"
}

Results are saved to sqli_findings.json.

Week 4 – XSS Testing Module
Objective

Inject JavaScript payloads to detect Reflected, Stored, and DOM-based XSS.

Supported XSS Types

Reflected XSS

Detects payload reflected unescaped in response.

Stored XSS

Clears stored data before testing.

Checks persistent script injection.

DOM-Based XSS

Injects payload into URL fragment.

Detects dangerous DOM sinks such as:

document.write()

innerHTML

eval()

location.hash

setTimeout()

Detection Logic

Inject payload into text input fields.

Compare response with baseline.

Check:

Direct payload reflection

HTML encoding (sanitized input)

DOM sink patterns

Classify vulnerability type.

Assign High severity.

Output

Structured findings saved to:

xss_findings.json

Each entry includes:

Page

Endpoint

Method

Payload

XSS type

Evidence

Severity