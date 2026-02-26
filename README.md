# WebScanPro-Web-Applicaon-Security-Testing-Tool-Batch13


## 📌 Project Overview
WebScanPro is a Python-based automated web security testing tool developed as part of an internship project.  
It is designed to identify common web vulnerabilities such as SQL Injection and Cross-Site Scripting (XSS).

The tool was tested using DVWA (Damn Vulnerable Web Application) running on a local XAMPP server.

---

## 🎯 Milestone-1: Target Scanning

In this phase, the following tasks were completed:

- Target application setup (DVWA)
- Web crawling to extract internal links
- Form detection and input field identification
- Storing scan results in JSON format

<img width="836" height="608" alt="web xampp start" src="https://github.com/user-attachments/assets/73d2b38d-0c5c-4ddf-9e81-85f8e9bdb2a5" />

Modules Used:
- crawler.py

Output:
- scan_results.json

---

## 🎯 Milestone-2: Vulnerability Detection

In this phase, automated vulnerability testing modules were implemented:

### 🔴 SQL Injection Detection
- Injected multiple SQL payloads
- Analyzed server responses
- Detected possible SQL injection vulnerabilities
- Assigned severity level
- Generated sqli_report.json

### 🟠 Cross-Site Scripting (XSS) Detection
- Injected script payload
- Checked for reflected script execution
- Detected XSS vulnerability
- Generated xss_report.json

---

## 📄 Final Report Generation
All scan results are combined into a single structured report:

- output.txt

---

## 🛠 Technologies Used

- Python 3
- Requests library
- BeautifulSoup (bs4)
- JSON
- DVWA
- XAMPP

---

## 📂 Project Structure

WEBSCANPRO1/
│
├── crawler.py  
├── sqli_tester.py  
├── xss_tester.py  
├── generate_report.py  
├── main.py  
├── scan_results.json  
├── sqli_report.json  
├── xss_report.json  
├── output.txt  

---

## ▶️ How to Run

Step 1: Start XAMPP (Apache & MySQL)  
Step 2: Open DVWA in browser  
Step 3: Run the main file
