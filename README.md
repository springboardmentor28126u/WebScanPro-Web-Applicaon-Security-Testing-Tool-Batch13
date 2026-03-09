WebScanPro – Web Application Security Testing Tool (Batch 13)
📖 Project Overview

WebScanPro is an automated web application security testing tool designed to identify common vulnerabilities aligned with the OWASP Top 10.

The system simulates real-world attack vectors against a web application, analyzes responses, and generates structured vulnerability reports with recommended mitigation strategies.

The tool currently focuses on detecting:

SQL Injection (SQLi)

Cross-Site Scripting (XSS)

Authentication weaknesses

Input validation flaws

Potential DOM-based risks

Future extensions include testing for:

Broken Authentication

Insecure Direct Object References (IDOR)

Access control issues

Session management vulnerabilities

🛠 Environment Setup
Local Setup Using XAMPP

The testing environment was configured locally to safely simulate vulnerabilities.

Steps performed:

Installed XAMPP (Apache + MySQL)

Started Apache and MySQL services

Downloaded DVWA (Damn Vulnerable Web Application)

Deployed DVWA inside the XAMPP htdocs directory

Accessed the application at:

http://localhost/dvwa

Set DVWA Security Level to LOW for controlled vulnerability testing.

🎯 Target Applications

The following intentionally vulnerable applications were explored:

Application	Purpose
DVWA	Primary testing platform
OWASP Juice Shop	Modern web security lab
bWAPP	Additional vulnerability practice

While all were explored, DVWA was used for automated testing implementation.

🔍 Exploration of Target Application (DVWA)
1️⃣ Structure Analysis

DVWA follows a traditional web application architecture:

Backend: PHP

Database: MySQL

Server: Apache

Input handling: GET and POST parameters

Multiple built-in vulnerability modules

The architecture directly processes user input in server-side scripts, making it suitable for vulnerability testing.

For comparison:

OWASP Juice Shop uses Node.js + Angular with REST APIs.

bWAPP follows a structure similar to DVWA.

⚙️ Application Functionality Analysis

The following functional components were observed:

Login authentication system

User data retrieval modules

Comment/message submission forms

User management features

Each of these modules processes user-supplied input, which becomes potential attack surfaces for testing vulnerabilities.

🧪 Manual Vulnerability Testing

Before building the automated scanner, manual testing was performed to understand how vulnerabilities behave.

🔹 SQL Injection (SQLi)

Testing Process

Entered a normal user ID → returned expected record.

Injected payload:

1' OR '1'='1

Observed Result

The application returned all user records.

Conclusion

User input was directly inserted into SQL queries.

No proper input validation was implemented.

SQL error messages were exposed.

This confirmed the presence of SQL Injection vulnerabilities.

🔹 Cross-Site Scripting (XSS)
Reflected XSS

Injected payload:

<script>alert(1)</script>

Result

Script executed immediately in the browser.

Conclusion

User input was reflected in the response without sanitization.

Stored XSS

Injected the same payload into the message field.

Result

Script executed again after page reload.

Conclusion

Malicious input was stored in the database and rendered later.

This confirmed Stored XSS vulnerability.

🔹 Authentication Weakness

Tested authentication logic using malicious input.

Payload used:

admin' OR '1'='1

Result

Login bypass occurred without a valid password.

Conclusion

SQL injection vulnerability existed in authentication logic.

No rate limiting or account lockout mechanism was implemented.

This indicates susceptibility to brute-force and authentication bypass attacks.

🔹 Authorization Testing

Tested access control restrictions.

Steps performed:

Logged in as a non-admin user.

Verified that admin modules were hidden from navigation.

Attempted direct access via URL manipulation.

Result

Server blocked unauthorized access.

Conclusion

Proper server-side access control was implemented for restricted modules.

🤖 Automated Scanner Implementation

The project then moved from manual testing to automated security scanning.

The automated scanner performs the following workflow:

Login → Crawl → Extract Forms → Test SQL Injection → Test XSS → Generate Report
🔹 Module 1 – Authentication Handler

The tool logs into DVWA automatically by:

Creating an authenticated HTTP session

Extracting CSRF tokens

Submitting login credentials programmatically

Setting the security level to LOW

This allows automated scanning of protected pages.

🔹 Module 2 – Target Scanning (Crawler)

The crawler module:

Discovers internal application pages

Extracts hyperlinks from HTML

Restricts crawling to the target domain

Avoids logout endpoints and duplicate links

This builds the attack surface map of the application.

🔹 Module 3 – Form Extraction

The extractor module:

Identifies HTML forms

Collects form actions and HTTP methods

Extracts input field names and types

These inputs become injection points for security testing.

🔹 Module 4 – SQL Injection Detection

The SQL injection testing module:

Sends baseline requests to observe normal behavior

Injects SQL payloads into parameters

Detects error-based SQL injection via database error messages

Detects blind SQL injection using logical condition testing

Compares response length differences to confirm anomalies

Detected vulnerabilities are stored with evidence and remediation suggestions.

🔹 Module 5 – XSS Detection

The XSS testing module:

Injects JavaScript payloads into form inputs

Checks if payloads are reflected in the response

Reloads pages to detect stored XSS

Flags risky DOM patterns like innerHTML and document.write

Tests both form inputs and URL parameters

📊 Output and Reporting

After scanning is complete, the tool generates a structured vulnerability report.

Example output format:

{
  "sqli": [...],
  "xss": [...]
}

The report includes:

Vulnerability type

Affected endpoint

Parameter name

Payload used

Severity level

Suggested remediation techniques

Reports are saved in:

data/vulnerabilities.json
