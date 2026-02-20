                                                                               🔐 Project Title
                                                                   WebScanPro: Web Application Security Testing Tool
🎯 Objective:

.The objective of Week 1 was to:
.Define the project goals and expected outcomes.
.Set up a local testing environment.
.Deploy an intentionally vulnerable web application.
.Explore the structure and potential security flaws manually.

🧠 Project Goal

.To develop an automated web application security testing tool using Python that can detect common vulnerabilities such as:
.SQL Injection
.Cross-Site Scripting (XSS)
.Broken Authentication
.Insecure Direct Object References (IDOR)

🛠 Tools Used in Week 1

Tool	Purpose
XAMPP	Local server environment (Apache + MySQL)
DVWA	Vulnerable web application for testing
VS Code	Development environment
Python	Programming language for scanner development

⚙ Environment Setup

.1️⃣ Installing XAMPP
.Installed XAMPP for Windows.
.Started Apache and MySQL services.
.Verified setup using:
.http://localhost

.2️⃣ Deploying DVWA
.Copied DVWA folder into:
.C:\xampp\htdocs\
Accessed DVWA using:
http://localhost/dvwa
Created/reset database.
Logged in using default credentials:

Username: admin
Password: password
Set DVWA security level to LOW for testing.

🔎 Manual Exploration of DVWA

The application was manually explored to understand:
Available modules
URL structures
Input fields
Form submissions
Query parameters (e.g., ?id=1)

Identified Vulnerable Modules:

SQL Injection
Reflected XSS
Stored XSS
Brute Force
Command Injection
File Upload

📌 Outcome of Week 1
.Successfully set up a local testing environment.
.Understood the structure and behavior of a vulnerable web application.
.Identified potential injection points for automated testing.
.Prepared the foundation for scanner development.
                                                                                                   week-2
                                                                        
Project Structure (Week-2)
├── main.py
├── crawler.py
└── scan_results.txt   (auto-created)

1️⃣ crawler.py (Target Scanning Module)
->This file contains the crawler logic.
program:-
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
def crawl(url):
    print(f"\nScanning Target: {url}\n")
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        with open("scan_results.txt", "w") as file:
            file.write("=== WebScanPro Target Scan Results ===\n\n")
            file.write("Links Found:\n")
            print("Links Found:")
            for link in soup.find_all("a"):
                href = link.get("href")
                if href:
                    full_url = urljoin(url, href)
                    print(full_url)
                    file.write(full_url + "\n")
            file.write("\nForms Found:\n")
            print("\nForms Found:")
            for form in soup.find_all("form"):
                form_details = str(form)
                print(form_details)
                file.write(form_details + "\n")
        print("\nScan completed. Results saved in scan_results.txt")
    except Exception as e:
        print("Error occurred:", e)

2️⃣ main.py (Program Entry Point)
->This file runs the crawler.

from crawler import crawl
if __name__ == "__main__":
    target_url = "http://localhost/dvwa/"
    crawl(target_url)

3️⃣ Command You Executed
.In VS Code terminal:
python main.py

📌 What This Code Did (Week-2 Purpose)

✔ Connected to DVWA
✔ Downloaded webpage HTML
✔ Extracted all links
✔ Extracted all forms
✔ Printed them in terminal
✔ Saved results to scan_results.txt

📄 Example Output (scan_results.txt)
=== WebScanPro Target Scan Results ===

Links Found:
http://localhost/dvwa/login.php
http://localhost/dvwa/vulnerabilities/sqli/
http://localhost/dvwa/vulnerabilities/xss_r/

Forms Found:
<form action="login.php" method="post">
...

🎯 What You Completed in Week-2

->You successfully implemented:
.HTTP communication
.HTML parsing
.Link discovery
.Form extraction
.Metadata storage
.This completes :  Target Scanning Module
