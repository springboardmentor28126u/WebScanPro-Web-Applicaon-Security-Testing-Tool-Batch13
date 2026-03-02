# 🚀 WebScanPro  
### Automated Web Application Security Testing Tool  

WebScanPro is a modular automated web vulnerability scanner developed as part of an internship project to understand how security testing tools operate internally.  

The tool is designed to scan a target web application, identify input surfaces, inject test payloads, analyze server responses, and generate structured vulnerability findings.  

DVWA (Damn Vulnerable Web Application) is used as the controlled testing environment for development and validation.

---

# 📌 Milestone 1 – Project Initialization & Target Scanning

Milestone 1 focused on establishing the testing environment and developing the foundational crawling module required for automated vulnerability detection.

---

# 📅 Week 1 – Project Initialization & Environment Setup

## 🎯 Project Goals and Objectives

The objective of WebScanPro is to design a scalable and modular vulnerability scanning tool capable of detecting common web application vulnerabilities aligned with OWASP Top 10 standards.

### Key Goals

- Understand web application security fundamentals  
- Study HTTP request–response lifecycle  
- Explore vulnerability patterns in web forms and URLs  
- Perform manual testing before automation  
- Design structured scanning workflow  

---

## 🛠 Development Environment Setup

To build a secure and controlled lab environment, the following tools were installed:

### Tools & Technologies

- **Python** – Core programming language  
- **Virtual Environment (venv)** – Dependency isolation  
- **Requests Library** – HTTP communication  
- **BeautifulSoup** – HTML parsing  
- **Selenium** – Future browser automation  
- **Docker Desktop** – Containerized deployment  

---

## 🐳 DVWA Deployment Using Docker

DVWA was deployed using Docker to simulate a vulnerable web application.

It is useful because:
- Provides isolated environment
- No manual configuration of Apache/PHP/MySQL
- Easy start and stop management
- Safe vulnerability testing setup

## 🔎 Manual Exploration & Vulnerability Understanding

DVWA was manually explored to understand:

- Website navigation flow
- Authentication mechanisms
- Forms and input parameters
- Built-in vulnerable modules

 ### Manual Testing Conducted:
- SQL Injection
- Reflected XSS
- Stored XSS
- Command Injection

This helped in understanding how vulnerabilities behave before automating detection logic.

# 📅 Week 2 – Target Scanning Module Development

Week 2 focused on automating the discovery of attack surfaces through implementation of the crawler module.

## 🕷 Crawler Module Design (crawler.py)

The crawler module was implemented to automatically:

- Discover internal web pages
- Extract hyperlinks
- Identify HTML forms
- Detect input fields
- Capture GET and POST parameters

This automated the process of identifying injection points.

## 🧩 HTML Parsing Using BeautifulSoup

The crawler uses BeautifulSoup to:

- Parse HTML response content
- Extract <a> tags for link discovery
- Extract <form> elements
- Collect <input> field attributes

This allows the scanner to programmatically locate interactive components.

## 📊 Metadata Structuring for Testing Modules

The extracted data is structured into organized metadata including:

- Form action URLs
- Input field names
- HTTP request methods (GET/POST)
- Discovered endpoints

This structured information is then passed to vulnerability testing modules such as:

~ SQL Injection Scanner

~ XSS Scanner

## 🔁 Workflow Established by End of Week 2

By the end of Week 2, the system could:

- Connect to the target application
- Crawl pages automatically
- Extract forms and parameters
- Prepare structured input data for testing modules

This created the technical foundation required for implementing automated vulnerability detection in the next milestone.

# ✅ Milestone 1 Outcome

- Fully configured testing lab environment
- Successful deployment of DVWA
- Manual validation of vulnerabilities
- Implementation of automated crawler
- Structured attack surface mapping

Milestone 1 successfully established the core infrastructure and discovery engine required for WebScanPro.


# 📌 Milestone 2 – Vulnerability Detection Engine (SQLi & XSS)

Milestone 2 focused on transforming the passive discovery engine into an active security testing tool. This phase involved developing automated modules to detect high-risk vulnerabilities—SQL Injection and Cross-Site Scripting (XSS)—by simulating real-world attack vectors against the attack surface identified during Milestone 1.

---

# 📅 Week 3 – SQL Injection Testing Module

## 🎯 SQL Injection Testing Objectives

The goal was to identify database-level flaws where malicious SQL queries could be executed via user input.

### Key Goals:

* Inject crafted SQL payloads into form fields and URL parameters.


* Analyze server responses for database-specific error patterns.


* Identify vulnerable injection points and suggest mitigation strategies.



---

## 🛠 SQLi Scanner Implementation (`sqli_scanner.py`)

The scanner utilizes an **error-based detection** strategy to identify vulnerabilities:

### Detection Mechanism:

* **Payload Injection**: Loads malicious strings (e.g., `' OR '1'='1`) from a dedicated `sqli_payload.txt` file.
* **Signature Analysis**: Scans HTML response bodies for known database error strings such as "mysql_fetch", "syntax error", or "unclosed quotation mark".
* **Intelligent Filtering**: Automatically skips non-injectable parameters like `user_token` (CSRF tokens) and `submit` buttons to improve scan efficiency.

---

# 📅 Week 4 – Cross-Site Scripting (XSS) Testing Module

## 🎯 XSS Testing Objectives

Week 4 focused on identifying client-side vulnerabilities where unvalidated user input is reflected and executed as JavaScript in the victim's browser.

### Key Goals:

* Inject JavaScript-based payloads into discovered form fields and URLs.


* Detect reflected scripts through response analysis.


* Record vulnerable endpoints and provide XSS prevention tips.



---

## 🕷 XSS Scanner Design (`xss_scanner.py`)

The XSS module was designed to be robust and method-aware:

### Module Features:

* **Method Support**: The scanner tests both **GET** and **POST** requests based on the form data captured by the crawler.
* **Reflection Logic**: It validates a vulnerability if the injected payload (e.g., `<script>alert('XSS')</script>`) is found verbatim within the returned HTML.
* **Payload Diversity**: Uses various triggers, including script tags and event handlers (e.g., `onerror`), to bypass basic filters.

---

## 📊 Result Consolidation and Reporting

To prepare for the **Week 7 Security Report**, all findings are aggregated into a unified reporting format.

### Data Structure (`results.json`)

Each identified vulnerability is saved with critical metadata:

* **Vulnerability Type**: Categorized as SQL Injection or Cross-Site Scripting.
* **Affected Endpoint**: The specific URL where the flaw was found.
* **Parameter & Payload**: The exact input field and string that triggered the flaw.
* **Severity Level**: Assigned a **HIGH** severity rating due to potential impact.

---

## 🔁 Workflow Established by End of Week 4

By the end of Milestone 2, the system could:

* **Authenticate**: Maintain a valid session and security level on DVWA.
* **Probe**: Programmatically test hundreds of injection points across discovered pages.
* **Verify**: Confirm vulnerabilities through active response analysis rather than simple blind guessing.
* **Log**: Generate a structured JSON database containing all confirmed security flaws.

---

# ✅ Milestone 2 Outcome

* Automated SQL Injection detection using signature matching.
* Reflected XSS detection through reflection analysis.
* Successful identification of flaws across different HTTP methods (GET/POST).
* Establishment of a structured vulnerability findings database in `reports/results.json`.

Milestone 2 successfully turned the passive discovery engine into an active security testing tool capable of identifying high-risk vulnerabilities.
