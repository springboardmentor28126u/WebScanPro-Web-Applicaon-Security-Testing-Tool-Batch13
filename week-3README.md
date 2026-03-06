# Week 3 – SQL Injection Testing Module

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