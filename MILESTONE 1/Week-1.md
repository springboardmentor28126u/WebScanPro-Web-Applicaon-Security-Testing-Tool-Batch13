# WebScanPro – Automated Web Application Security Scanner

---

## Introduction

WebScanPro is an automated web application security testing tool developed as part of an internship project to understand the internal working of vulnerability scanners and modern security assessment methodologies.

The primary objective of this project is to design and implement a modular scanning system capable of identifying common web application vulnerabilities based on the OWASP Top 10 standards.

The tool scans a target web application — DVWA (Damn Vulnerable Web Application) — and performs both automated and controlled manual testing to detect vulnerabilities such as:

- SQL Injection
- Cross-Site Scripting (XSS)
- Command Injection

### Project Focus

- Simulating real-world attack techniques  
- Analyzing HTTP responses  
- Generating structured vulnerability reports  

---

# Week 1 – Project Initialization & Environment Setup

## Objective of Week 1

Week 1 focused on establishing the foundational infrastructure required for developing WebScanPro.

### Key Goals

- Define project objectives  
- Create controlled testing environment  
- Install and configure required tools  
- Deploy vulnerable target application  
- Understand core vulnerabilities manually  

This phase created a stable and secure lab environment for safe vulnerability testing and future automation.

---

# 1. Software & Tools Installed

## A. Python

Python is used to build the automated scanner.
Installation verified using:

python --version
pip --version

Python is responsible for:
- Sending HTTP requests
- Automating login
- Crawling web pages
- Performing vulnerability tests (later stages)

Responsibilities

- Sending HTTP requests
- Automating login
- Crawling web pages
- Performing vulnerability tests

## B. Virtual Environment (venv)

Created to isolate project dependencies.

- Creation
python -m venv venv

- Activation (Windows)
venv\Scripts\activate

- Purpose

--> Keeps project libraries separate

--> Avoids dependency conflicts

--> Ensures reproducibility

## C. Installed Python Libraries
- pip install requests

- pip install beautifulsoup4

- pip install selenium

Library Purpose

- requests	Sends HTTP GET & POST requests
- beautifulsoup4	Parses HTML to extract forms & links
- selenium	Browser automation

A requirements.txt file was created to manage dependencies.

# 2. Docker & DVWA Setup

## A. Docker Desktop

Used to run DVWA in an isolated container.

- Verification
docker --version

- Purpose

--> Runs DVWA in isolation

--> No manual Apache/PHP/MySQL setup

--> Easy start/stop environment

## B. DVWA Deployment
- Pull Image
docker pull vulnerables/web-dvwa

- Run Container
docker run -d -p 8081:80 vulnerables/web-dvwa


-d → Run in background

-p 8081:80 → Map local port 8081 to container port 80

Access DVWA at:

http://localhost:8081

~ What is DVWA?

DVWA (Damn Vulnerable Web Application) is an intentionally insecure web application designed for:

- Security testing practice
- Learning vulnerabilities
- Developing scanners
- Contains Vulnerabilities
- SQL Injection
- XSS
- Command Injection
- File Inclusion
- Brute Force
- CSRF

DVWA serves as a safe target environment.

# 3. Project Folder Structure

WebScanPro/
│
├── venv/
├── scanner/
│   ├── __init__.py
│   ├── crawler.py
│   ├── sqli_scanner.py
│   └── xss_scanner.py
│
├── reports/
├── main.py
└── requirements.txt

## A. venv/

Contains isolated Python dependencies.
Not uploaded to GitHub.

## B. scanner/

Contains core vulnerability detection modules.

### B.1. init.py

Makes scanner a Python package.

from scanner.crawler import crawl

### B.2. crawler.py

Responsible for exploring target website.

- Functions

--> Discover links
--> Extract forms
--> Identify input fields
--> Detect GET/POST parameters

- Process

--> Send HTTP request
--> Parse HTML using BeautifulSoup
--> Extract <a>, <form>, <input> tags
--> Return structured data

### B.3. sqli_scanner.py

- Detects SQL Injection vulnerabilities.
- Payload Used
' OR '1'='1
- Detection Logic
- Submit modified request
- Analyze response for:
- SQL errors
- Authentication bypass
- Abnormal behavior

### B.4. xss_scanner.py

- Detects Cross-Site Scripting vulnerabilities.
- Payload
<script>alert('XSS')</script>
- Detection Logic
- Inject payload
- Submit form
- Check if script reflects unescaped

## C. reports/

- Stores scan results.
- Future implementation:

--> JSON reports

--> HTML reports

## D. main.py

- Entry point of the application
Controls execution flow
- Performs:
--> Connection check
--> Login automation
--> Calls crawler
- When running:
python main.py

Execution starts from this file.


## E. requirements.txt

Lists dependencies.

pip install -r requirements.txt

### 4. Manual Vulnerability Testing (DVWA)

The following section describes the manual testing of vulnerabilities performed on DVWA (Damn Vulnerable Web Application). All tests were conducted with the security level set to Low in order to clearly observe insecure behaviors and understand how vulnerabilities occur due to improper input handling.


## A. SQL Injection
- Introduction
SQL Injection is a vulnerability that occurs when user input is directly included in a database query without proper validation or parameterization. This allows an attacker to manipulate the structure of the SQL query and retrieve unauthorized data.
- Manual Testing Procedure
The SQL Injection module was accessed from the DVWA interface. Initially, a normal input value of 1 was entered into the User ID field. The application returned a single user record corresponding to that ID.
After verifying normal behavior, a malicious input was provided:
1' OR '1'='1





- Result
The application displayed multiple user records instead of one. This confirmed that the input was not properly validated and that the system was vulnerable to SQL Injection.
- Conclusion
The vulnerability exists because user input is directly embedded into the SQL statement without using prepared statements or parameterized queries.

## B. Reflected XSS
- Introduction
Reflected Cross-Site Scripting occurs when user input is immediately reflected back in the webpage without proper sanitization, allowing execution of malicious JavaScript code.
- Manual Testing Procedure
The XSS (Reflected) module was opened. The following payload was entered in the input field:
<script>alert('XSS')</script>
The form was then submitte

- Result
An alert box appeared in the browser. This confirmed that the script was executed successfully, indicating the presence of a reflected XSS vulnerability.
- Conclusion
The vulnerability exists because the application fails to sanitize or escape HTML special characters before rendering user input.

## C. Stored XSS
- Introduction
Stored XSS is a persistent form of XSS in which malicious input is stored in the database and executed whenever the page is accessed.

- Manual Testing Procedure
The XSS (Stored) module was accessed. The following payload was entered into the message field:
<script>alert('Stored')</script>
The form was submitted and the page was refreshed.

- Result
The alert box appeared each time the page was loaded. This confirmed that the malicious script was permanently stored and executed repeatedly.
- Conclusion
Stored XSS is more dangerous than reflected XSS because it affects every user who accesses the page. The vulnerability exists due to lack of input validation before storing data.


## D. Command Injection
- Introduction
Command Injection occurs when user input is directly passed to system-level commands without validation, allowing execution of arbitrary operating system commands.
- Manual Testing Procedure
The Command Injection module was opened. First, a normal IP address such as:
127.0.0.1

was entered, and the application displayed the ping result.
Then, the following malicious input was provided:
127.0.0.1; ls

- Result
The output displayed not only the ping result but also the list of files in the directory. This confirmed that arbitrary system commands could be executed.
- Conclusion
The vulnerability exists because the application does not validate or sanitize input before passing it to the system command.

### 5. Outcome of Week 1

By the end of Week 1, the foundational environment and project structure for WebScanPro were successfully established.
The system was capable of:
- Successfully installing and configuring Python and required libraries
- Creating and activating a virtual environment for dependency isolation
- Installing and running Docker
- Deploying and accessing DVWA** (Damn Vulnerable Web Application)** in a controlled environment
- Verifying successful connection to the target application (HTTP status validation)
- Understanding and manually testing core vulnerabilities such as:
--> SQL Injection
--> Reflected XSS
--> Stored XSS
--> Command Injection

- Designing the project folder structure
- Setting up the core execution file (main.py)
- Preparing the scanner architecture for future automation modules


Week 1 successfully completed the Environment Setup and Vulnerability Understanding Phase, creating a secure lab setup and establishing the technical groundwork required for automated scanning implementation in the upcoming weeks.
