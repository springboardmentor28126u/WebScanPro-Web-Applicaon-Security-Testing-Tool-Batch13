# WebScanPro – Automated Web Application Security Scanner

---

## Introduction

WebScanPro is an automated web application security testing tool developed to understand the internal working of vulnerability scanners and modern security assessment methodologies. The primary objective of this project is to design and implement a modular scanning system capable of identifying common web application vulnerabilities based on the OWASP Top 10 standards.
The tool scans a target web application — DVWA (Damn Vulnerable Web Application) in our case — and performs both automated and controlled manual testing to detect vulnerabilities such as SQL Injection and Cross-Site Scripting (XSS). The project focuses on simulating real-world attack techniques, analyzing HTTP responses, and generating structured vulnerability reports.

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

## B. Virtual Environment (venv)

Created to isolate project dependencies.

- Creation
python -m venv venv

- Activation (Windows)
venv\Scripts\activate

- Purpose
  

Keeps project libraries separate


Avoids dependency conflicts


Ensures reproducibility


## C. Installed Python Libraries


 pip install requests
 
 pip install beautifulsoup4
 
 pip install selenium
 

- Library Purpose:
  

 requests	Sends HTTP GET & POST requests
 
 beautifulsoup4	Parses HTML to extract forms & links
 
 selenium	Browser automation
 

A requirements.txt file was created to manage dependencies.

# 2. Docker & DVWA Setup

## A. Docker Desktop

Used to run DVWA in an isolated container.

- Verification
docker --version

- Purpose

 Runs DVWA in isolation
 
 No manual Apache/PHP/MySQL setup

 
 Easy start/stop environment

<img width="1569" height="884" alt="image" src="https://github.com/user-attachments/assets/a65ffc88-e64a-40af-9248-f14a4de2c139" />

## B. DVWA Deployment

DVWA was deployed using Docker to create a safe and isolated testing environment.

The DVWA image was downloaded using:

docker pull vulnerables/web-dvwa

This command fetched the pre-configured DVWA application containing Apache, PHP, and MySQL.

The container was started using:
docker run -d -p 8081:80 vulnerables/web-dvwa

Here:
- -d runs the container in background
- -p 8081:80 maps local port 8081 to port 80 inside the container

Since DVWA runs on port 80 inside the container, accessing:
http://localhost:8081
opens the DVWA application in the browser.
Docker was used to ensure easy setup, isolation, and safe vulnerability testing.


# ~ What is DVWA?

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

<img width="650" height="337" alt="image" src="https://github.com/user-attachments/assets/b87ff458-5da0-44fe-bcec-cda558fa79ea" />


# 3. Project Folder Structure

<img width="524" height="442" alt="image" src="https://github.com/user-attachments/assets/0eb67b0b-e372-4978-9d88-c7d9913a60b4" />


## A. venv/
This folder contains the virtual environment created for the project.
Purpose
The purpose of this folder is to:
- Maintain isolated Python dependencies

- Avoid conflicts with system-wide Python packages

- Ensure consistent execution across systems


It contains installed libraries such as:
- requests

- beautifulsoup4

- other required modules


This folder is not part of the core application logic and is usually not uploaded to GitHub.


## B. scanner/

Contains core vulnerability detection modules.

### B.1. init.py

Makes scanner a Python package.

from scanner.crawler import crawl

### B.2. crawler.py

Responsible for exploring target website.

- Functions

 Discover links
 
 Extract forms
 
 Identify input fields
 
 Detect GET/POST parameters
 

- Process

 Send HTTP request

 
 Parse HTML using BeautifulSoup

 
 Extract <a>, <form>, <input> tags

 
 Return structured data

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


 JSON reports
 
 HTML reports

## D. main.py

- Entry point of the application
Controls execution flow
- Performs:

 Connection check
 
 Login automation
 
 Calls crawler
 
- When running:
python main.py

Execution starts from this file.


## E. requirements.txt

Lists all required Python libraries
Allows installation using:

pip install -r requirements.txt

Ensures environment can be recreated easily.


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

<img width="844" height="357" alt="image" src="https://github.com/user-attachments/assets/79810ff4-33dd-46e7-aaba-fdf5c24bf5d5" />

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
<img width="691" height="319" alt="image" src="https://github.com/user-attachments/assets/3e75a925-7243-4876-b7a7-10b66f6089a2" />


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

<img width="424" height="385" alt="image" src="https://github.com/user-attachments/assets/b5c739d6-33da-4620-9de2-0741ff450cfd" />

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
<img width="540" height="425" alt="image" src="https://github.com/user-attachments/assets/418428dd-69ba-458d-8847-858dbd41d83b" />

### 5. Outcome of Week 1

By the end of Week 1, the foundational environment and project structure for WebScanPro were successfully established.
The system was capable of:
- Successfully installing and configuring Python and required libraries
- Creating and activating a virtual environment for dependency isolation
- Installing and running Docker
- Deploying and accessing DVWA** (Damn Vulnerable Web Application)** in a controlled environment
- Verifying successful connection to the target application (HTTP status validation)
- Understanding and manually testing core vulnerabilities such as:
  
SQL Injection

Reflected XSS

Stored XSS

Command Injection

- Designing the project folder structure
- Setting up the core execution file (main.py)
- Preparing the scanner architecture for future automation modules


Week 1 successfully completed the Environment Setup and Vulnerability Understanding Phase, creating a secure lab setup and establishing the technical groundwork required for automated scanning implementation in the upcoming weeks.
