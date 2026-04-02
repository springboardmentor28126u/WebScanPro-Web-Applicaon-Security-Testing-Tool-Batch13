📌 WebScanPro – Web Application Security Testing Tool
📖 Overview

WebScanPro is a web application security testing tool designed to identify common vulnerabilities in web applications such as SQL Injection, XSS, CSRF, and authentication flaws. It automates scanning, detects issues, and provides suggestions to improve security.

🎯 Objectives
Detect common web vulnerabilities
Automate security testing
Provide detailed reports
Improve application security awareness
🛠️ Technologies Used
Python
Flask (for web interface)
Requests Library
BeautifulSoup
SQLite / MySQL
HTML, CSS (for dashboard)

## Week 1 – Project Setup

### 📖 Overview
In Week 1, we focused on setting up the foundation required for building the report generation system and understanding how security reports should be structured.

### 🛠️ Work Done
- Initialized the project repository using Git and GitHub.
- Set up Python development environment.
- Installed required libraries for future report generation (like HTML handling, file writing).
- Installed DVWA (Damn Vulnerable Web Application) for testing.
- Studied sample vulnerability reports to understand structure and format.
- Identified key components required in a report:
  - Vulnerability Name
  - Affected URL
  - Description
  - Severity Level
  - Suggested Fix

### 🎯 Outcome
- Environment successfully set up for development.
- Clear understanding of how security reports should be designed.
- Defined structure for report generation module.

---

## Week 2 – Target Scanning Module

🎯 Objective

Develop an automated crawler to scan the target application and extract important testing data.

🛠 Technologies Used

Python

requests library

BeautifulSoup (bs4)

Visual Studio Code

🔍 Crawler Features

The crawler:

Discovers internal web pages

Extracts hyperlinks

Identifies forms

Detects input fields (text, password, textarea, select)

Avoids visiting duplicate pages

📊 Metadata Collection

The crawler collects:

URL list

Form action

Form method (GET/POST)

Input name

Input type

This metadata is stored for future vulnerability testing modules.

▶ How to Run

Ensure Apache and MySQL are running

Open terminal in project folder

Run:

python crawler.py


Output will display discovered pages and form details

✅ Week 2 Outcome

✔ Automated web page discovery
✔ Form and input field extraction
✔ Structured metadata collection
✔ Ready for vulnerability testing module

📁 Project Structure
WebScanPro/
│
├── crawler.py
├── README.md
└── requirements.txt



## Week 3 – SQL Injection Testing Module

## Overview
In Week 3, we implemented a SQL Injection vulnerability scanner using Python. 
The scanner tests a web application by sending different SQL payloads and checking the response to detect possible SQL Injection vulnerabilities.

## Technologies Used
- Python
- Requests Library
- BeautifulSoup
- DVWA (Damn Vulnerable Web Application)
- XAMPP (Apache & MySQL)

## Project Files
sql_tester.py – Main program that performs SQL Injection scanning.

payloads.py – Contains a list of SQL Injection payloads used for testing.

results.json – Stores detected vulnerability results (created automatically after scanning).

## How the Scanner Works
1. The program logs into DVWA automatically.
2. It sets the DVWA security level to Low.
3. The scanner sends multiple SQL Injection payloads to the input field.
4. The server response is analyzed for SQL errors or abnormal output.
5. If a vulnerability is detected, the result is displayed in the terminal and saved in results.json.

## How to Run
1. Start XAMPP and run Apache and MySQL.
2. Open DVWA in your browser:
   http://localhost/dvwa
3. Run the scanner using the command:

python sql_tester.py

## Output
The scanner prints the detected SQL Injection vulnerability in the terminal and stores the result in the results.json file.

## Learning Outcome
- Understanding SQL Injection vulnerabilities
- Automating vulnerability scanning using Python
- Working with HTTP requests and responses

## Week 4 – Cross-Site Scripting (XSS) Testing Module

## Project

Web Application Security Testing Tool

## Objective

The objective of this module is to detect Cross-Site Scripting (XSS) vulnerabilities in a web application by sending malicious scripts (payloads) to input fields and checking if they are reflected in the response.

## Tools and Technologies Used

* Python
* Requests Library
* BeautifulSoup
* DVWA (Damn Vulnerable Web Application)
* XAMPP Server

## Files in this Module

* **xss_tester.py** – Main script used to perform the XSS scan.
* **xss_payloads.py** – Contains a list of XSS payloads used for testing.
* **xss_results.json** – Stores the detected vulnerabilities in JSON format.

## How It Works

1. The script logs into DVWA automatically.
2. It sets the DVWA security level to **Low**.
3. The scanner sends multiple XSS payloads to the vulnerable page.
4. The response from the server is analyzed.
5. If the payload is reflected in the response, it indicates a possible XSS vulnerability.
6. The detected results are stored in a JSON file.

## How to Run the Scanner

Open the terminal in the project folder and run:

```
python xss_tester.py
```

## Expected Output

The terminal will display whether a possible XSS vulnerability is detected and show the payload and tested URL.

## Conclusion

This module successfully demonstrates how automated tools can detect Cross-Site Scripting vulnerabilities in web applications.


## Week 5 – Authentication and Brute Force Testing

## Objective

The goal of this week is to test authentication mechanisms of the web application and identify weaknesses such as weak passwords or lack of login protection.

## Environment

* XAMPP Local Server
* DVWA (Damn Vulnerable Web Application)
* Python
* Requests Library

## Tasks Performed

* Analyzed the login functionality of the web application.
* Created a Python script to perform brute force testing on the login page.
* Used a list of common usernames and passwords to attempt login.
* Checked if the application allows unlimited login attempts.

## Tools and Technologies

* Python
* Requests Library
* DVWA Web Application

## Outcome

The brute force testing script was able to identify possible valid login credentials by trying multiple username and password combinations. This demonstrates the risk of weak authentication mechanisms.

## Security Recommendations

* Implement account lockout after multiple failed login attempts.
* Use strong password policies.
* Add CAPTCHA or multi-factor authentication to prevent automated attacks.

## Conclusion

This week's work helped in understanding authentication vulnerabilities and how brute force attacks can compromise user accounts if proper security controls are not implemented.


## Week 6 – Access Control and IDOR Testing

## Objective

The objective of this week is to test the web application for access control vulnerabilities such as Insecure Direct Object Reference (IDOR) and privilege escalation.

## Environment

* XAMPP Local Server
* DVWA (Damn Vulnerable Web Application)
* Python
* Requests Library

## Tasks Performed

* Analyzed application pages that use parameters such as user IDs.
* Modified ID parameters in the URL to check if unauthorized user data can be accessed.
* Tested horizontal privilege escalation by accessing other users' data.
* Attempted vertical privilege escalation by trying to access restricted pages.
* Created a Python script (`idor_test.py`) to automate testing of multiple ID values.

## Tools and Technologies

* Python
* Requests Library
* DVWA Web Application

## Outcome

By modifying the `id` parameter, different user records were accessed without proper authorization checks. This indicates a potential IDOR vulnerability in the application.

## Security Recommendations

* Implement proper access control checks on the server side.
* Use Role-Based Access Control (RBAC) to restrict access based on user roles.
* Implement Attribute-Based Access Control (ABAC) to ensure users can only access their own data.
* Avoid exposing direct object identifiers in URLs.

## Conclusion

This week's testing helped identify access control weaknesses in the application and demonstrated how improper authorization can lead to unauthorized data access.


## Week 7 – Integration and Final Scanner Execution

## Objective

The objective of Week 7 is to integrate all the previously developed security testing modules into a single web vulnerability scanner and perform a complete security scan of the test web application.

## Environment

* XAMPP Local Server
* DVWA (Damn Vulnerable Web Application)
* Python
* Requests Library
* Visual Studio Code

## Tasks Performed

* Integrated all vulnerability testing modules developed in previous weeks.
* Created a main scanner script (`main_scanner.py`) to run all modules sequentially.
* Executed the crawler module to discover application pages.
* Performed vulnerability testing for SQL Injection, Cross-Site Scripting (XSS), Brute Force Authentication, and IDOR.
* Stored the scan results in JSON files for analysis.

## Modules Integrated

* Website Crawler
* SQL Injection Testing
* Cross-Site Scripting (XSS) Testing
* Authentication / Brute Force Testing
* Access Control / IDOR Testing

## Outcome

The integrated scanner successfully executed all modules and generated results showing potential vulnerabilities in the test web application.

## Conclusion

Week 7 completed the development of the Web Application Security Testing Tool by integrating all vulnerability detection modules into a single scanner capable of performing automated security testing.
