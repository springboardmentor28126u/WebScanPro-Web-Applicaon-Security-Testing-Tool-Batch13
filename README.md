# WebScanPro-Web-Applicaon-Security-Testing-Tool-Batch13


## 📌 Project Overview
WebScanPro is a Python-based automated web security testing tool developed as part of an internship project.  
It is designed to identify common web vulnerabilities such as SQL Injection and Cross-Site Scripting (XSS).

The tool was tested using DVWA (Damn Vulnerable Web Application) running on a local XAMPP server.

---

## 🎯 Milestone-1: Setup ,Initiallization & Target Scanning

In this phase, the following tasks were completed:

- Target application setup (DVWA)
- Web crawling to extract internal links
- Form detection and input field identification
- Storing scan results in JSON format

<img width="836" height="608" alt="web xampp start" src="https://github.com/user-attachments/assets/73d2b38d-0c5c-4ddf-9e81-85f8e9bdb2a5" />

-Start XAMPP with Apache and MySQL Servers
<img width="1855" height="844" alt="Screenshot 2026-02-15 114009" src="https://github.com/user-attachments/assets/6bddeaf2-3a5e-4a05-bae1-502d78cff41b" />
-create a dvwa database in phpmyadmin

<img width="505" height="457" alt="Screenshot 2026-02-15 114320" src="https://github.com/user-attachments/assets/4edc41f1-4ae7-4228-98b9-ae66407f2385" />

-search localhost (dvwa)damn vulnerable web application for login page 

<img width="1671" height="960" alt="Screenshot 2026-02-15 113712" src="https://github.com/user-attachments/assets/0769a322-e792-4538-998b-86aaf2d081d4" />

-this is the home page of DVWAA ,first i did reset/setup the database

<img width="1121" height="842" alt="low security" src="https://github.com/user-attachments/assets/9b6de5c3-96f2-40b4-9df7-d1e1cf608c79" />
-later i set the security level to low succussfully



Modules Used:
- crawler.py
- scanner.py 
Output:
- scan_results.json (this file shows the scanned vulnarable URLs)

Outcomes for Milestone-1:
Successful deployment of DVWA
Manual validation of vulnerabilities
Implementation of automated crawler

---

## 🎯 Milestone-2: Vulnerability Detection (SQL & XSS testing)

In this phase, automated vulnerability testing modules were implemented:
Week -3 : ## 🔴 SQL Injection Detection

- Injected multiple SQL payloads
- Analyzed server responses
- Detected possible SQL injection vulnerabilities
- Assigned severity level
- Generated sqli_report.json

 week-4 : ## 🟠 Cross-Site Scripting (XSS) Detection
- Injected script payload
- Checked for reflected script execution
- Detected XSS vulnerability
- Generated xss_report.json

---

---

## 🎯 Milestone-3: Authentication & Access Control Testing

In this phase, advanced security testing modules were implemented to identify authentication and authorization vulnerabilities.

### 🔐 Authentication & Session Testing

* Tested for weak and default login credentials
* Simulated brute-force login attempts
* Checked for insecure session management
* Identified issues like session fixation and missing secure cookie flags
* Analyzed login responses for authentication bypass possibilities

Output:

* auth_report.json
  <img width="963" height="686" alt="Screenshot 2026-03-24 131125" src="https://github.com/user-attachments/assets/f952c6f4-7c49-4aa8-a2fa-2a9a503f9e46" />

---

### 🔑 Access Control & IDOR Testing

* Tested horizontal privilege escalation (accessing other user data)
* Tested vertical privilege escalation (normal user accessing admin features)
* Manipulated URL parameters to access unauthorized resources
* Detected IDOR (Insecure Direct Object Reference) vulnerabilities
* Verified access control enforcement in different endpoints

Output:

* idor_report.json
    <img width="1117" height="382" alt="Screenshot 2026-03-24 131209" src="https://github.com/user-attachments/assets/be7a9f98-73ef-4d87-9604-ed238e20534f" />

---

### 📊 Milestone-3 Output

* List of authentication vulnerabilities
* Unauthorized access endpoints detected
* Logs of tested payloads and responses

---

## 🎯 Milestone-4: Security Report & Documentation

In this final phase, all scan results were compiled into a professional report and project documentation was prepared.

### 📄 Security Report Generation

* Combined all vulnerability reports:

  * SQL Injection
  * XSS
  * Authentication issues
  * IDOR vulnerabilities
* Structured report includes:

  * Vulnerability Type
  * Affected URL
  * Severity Level (Low / Medium / High)
  * Description
  * Suggested Fix / Mitigation

Generated Files:

* final_report.html
* final_report.pdf

---

### 📊 Visualization (Optional Enhancement)

* Pie chart showing vulnerability distribution
* Bar chart for severity levels
* Improved readability with structured tables

---

### 📘 Documentation & Presentation

* Prepared detailed project documentation
* Explained architecture and workflow
* Added screenshots of:

  * Scanning process
  * Vulnerability detection
  * Final report output

---

### 🎥 Final Output

* Fully working automated security testing tool
* Detection of multiple vulnerabilities
* Professional report generation (HTML & PDF)
* Ready for demo and presentation

---

## 📂 Updated Project Structure

'''
WEBSCANPRO1/

│
├── crawler.py 
├── sqli_tester.py 
├── xss_tester.py 
├── auth_tester.py   ✅ 
├── idor_tester.py   ✅ 
├── generate_report.py 
├── main.py 
│
├── scan_results.json 
├── sqli_report.json 
├── xss_report.json 
├── auth_report.json   ✅ 
├── idor_report.json   ✅ 
│
├── final_report.html   ✅ 
├── final_report.pdf    ✅ 
│
├── output.txt
'''
---

## 🚀 Final Status

✅ Milestone-1 Completed
✅ Milestone-2 Completed
✅ Milestone-3 Completed
✅ Milestone-4 Completed

🎉 Project Successfully Implemented


## 📄 Final Report Generation
All scan results are combined into a single structured report:

- output.txt

---

## 🛠 Technologies Used

- Visual Studio Code
- Requests library
- BeautifulSoup (bs4)
- JSON
- DVWA
- XAMPP

---

## ▶️ How to Run

Step 1: Start XAMPP (Apache & MySQL)  
Step 2: Open DVWA in browser  
Step 3: Run the main file
