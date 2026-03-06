# Week 4 – Cross-Site Scripting (XSS) Testing Module

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
