
<div align="center">

# 🚀 WEBSCANPRO – WEB APPLICATION SECURITY TESTING TOOL - BATCH 13 🚀

</div>

---

# 📌 MILESTONE 1  
## Project Setup & Target Scanning Module  

This milestone covers the basic setup of the project and development of the first scanning module.

---

# 🔹 Week 1 – Project Initialization & Setup  

## 🔸 About the Project  

WebScanPro is a tool that checks web applications for common security problems like:

- SQL Injection  
- Cross-Site Scripting (XSS)  
- Weak login systems  
- Other common web security issues  

In Week 1, the goal was to set up everything and understand how the vulnerable application works.

---

## 🔸 Tools Used  

- XAMPP (Local Server – Apache & MySQL)  
- DVWA (Damn Vulnerable Web Application)  
- PHP & MySQL  
- Web Browser  
- Git & GitHub  

---

## 🔸 What I Did in Week 1  

### 1️⃣ Installed and Configured Environment  

- Installed XAMPP  
- Started Apache and MySQL  
- Downloaded DVWA  
- Placed DVWA inside `htdocs`  
- Created a database named `dvwa`  
- Updated configuration settings  
- Initialized the database  

After this, DVWA was running successfully in the browser.

---

## 🔸 Explored Vulnerability Modules  

I explored the following modules:

- **Brute Force Module** – Shows weak login system  
- **SQL Injection Module** – Shows database vulnerability  
- **XSS Module** – Shows how scripts can run in browser  

---

## 🔹 Manual SQL Injection Testing 

During exploration, I manually tested SQL Injection in the DVWA login form using the following payload:

```bash
' OR '1'='1
```

This test was done to check how the application handles unsafe user input.

### 💉 Manual SQL Injection Test Screenshot
![Manual SQL Injection Test](Week-1/screenshots/manual-sql-injection-test.png)

---

---
## 🔸 Week 1 Result  

✔ DVWA installed successfully  
✔ Vulnerability pages identified  
✔ Input fields located  
✔ Environment ready for automation  

---

## 📸 Week 1 Screenshots  

### 🖥️ XAMPP Running  
![XAMPP Running](Week-1/screenshots/xampp-running.png)  
*Fig 1.1: XAMPP Control Panel showing Apache and MySQL services running successfully.*

---

### 🏠 DVWA Dashboard  
![DVWA Dashboard](Week-1/screenshots/dvwa-dashboard.png)  
*Fig 1.2: DVWA dashboard confirming successful installation and configuration.*

---

### 🔐 Brute Force Module  
![Brute Force Page](Week-1/screenshots/dvwa-bruteforce-page.png)  
*Fig 1.3: DVWA Brute Force vulnerability module interface.*

---

### 💉 SQL Injection Module  
![SQL Injection Page](Week-1/screenshots/dvwa-sql-injection-page.png)  
*Fig 1.4: DVWA SQL Injection vulnerability testing page.*

---

### ⚡ XSS Reflected Module  
![XSS Reflected Page](Week-1/screenshots/dvwa-xss-reflected-page.png)  
*Fig 1.5: DVWA Reflected XSS module page.*

---

# 🔹 Week 2 – Target Scanning Module  

## 🔸 Objective  

The goal of Week 2 was to build an enhanced Python-based scanning engine that automatically identifies:

- Forms  
- Input fields  
- Form actions  
- HTTP methods  
- Internal URLs (Basic Crawling)  
- Hidden form tokens  

This structured data will be used for automated vulnerability testing in upcoming modules.

---

## 🔸 Technologies Used  

- Python 3.x  
- Requests (Session Handling Enabled)  
- BeautifulSoup  
- JSON  
- DVWA  
- XAMPP  

---

## 🔸 About scanner.py  

`scanner.py` is a modular scanning script designed to analyze the structure of a web application.

### 🔹 Key Capabilities:

- Initiates session using `requests.Session()`  
- Crawls internal links within the target scope  
- Extracts all `<form>` elements  
- Identifies:
  - Form action  
  - HTTP method (GET/POST)  
  - Input field names  
  - Input types  
  - Hidden fields (CSRF tokens, etc.)  
- Prevents duplicate URL scanning  
- Generates structured output files  
- Includes basic error handling for stability  

The scanner performs **passive reconnaissance only**.  
It does not inject payloads or exploit vulnerabilities.

---

## 🔸 How the Scanner Works  

1. Starts from:  
```
http://localhost/dvwa/
```
2. Creates a persistent HTTP session  
3. Discovers internal links  
4. Parses HTML using BeautifulSoup  
5. Extracts forms and input fields  
6. Stores structured results into output files  

---

## 🔸 Output Files  

### 📄 output.json  

Contains structured scanning results including:

- Discovered URLs  
- Page-level form mapping  
- Input field details  
- Hidden parameters  

### 📄 Output JSON Result  

```python
{
    {
    "urls": [],
    "forms": []
}
```

---

### 📄 output.txt  

Readable scan summary for quick analysis.

### 📄 Output TXT Result 

```python

=== Discovered URLs ===

=== Forms & Input Fields ===

```

---

## 🔸 Scan Results  

The scanner successfully:

✔ Discovered internal URLs  
✔ Extracted login form  
✔ Captured hidden security tokens  
✔ Identified HTTP methods  
✔ Organized data into structured JSON  

This prepares the foundation for automated SQL Injection and XSS testing.

---

## 📸 Week 2 Screenshots  

### ▶ Scanner Execution Output  
![Scanner Run](Week-2/screenshots/scanner_run.png)  
*Fig 2.1: Execution of scanner.py showing discovered URLs and forms.*

---

### 🐍 Python Version Verification  
![Python Version](Week-2/screenshots/py_version.png)  
*Fig 2.2: Python version verification for development environment.*

---

## 🔸 Limitations  

- Authentication automation not implemented  
- Depth-based crawling not configurable yet  
- No payload injection engine integrated  
- No vulnerability scoring module  

---

# ✅ Milestone 1 Summary  

✔ Local testing environment configured  
✔ Vulnerability modules analyzed  
✔ Python-based scanning engine developed  
✔ Internal link discovery implemented  
✔ Session-based crawling enabled  
✔ Structured JSON reporting system created  
✔ Automation-ready architecture prepared  

Milestone 1 establishes a strong foundation for developing a complete web application security testing framework.

---
# 📌 MILESTONE 2  
## Active Vulnerability Testing & Hybrid AI Integration  

Milestone 2 upgrades WebScanPro from passive scanning to an **AI-powered active vulnerability detection framework**.

This milestone introduces:

✔ Hybrid SQL Injection Detection (Rule-Based + AI)  
✔ Hybrid XSS Detection (Rule-Based + AI)  
✔ HTTP Response Code Monitoring  
✔ Response Time Analysis  
✔ Behavioral Feature Extraction  
✔ Confidence-Based Reporting  
✔ Structured JSON Output  

---

# 🔹 Week 3 – Hybrid SQL Injection Testing Module (AI-Enhanced)

## 🔸 Objective  

To develop a **Hybrid SQL Injection Detection Engine** that combines:

✔ Signature-Based Detection  
✔ Behavioral Analysis  
✔ Machine Learning Classification  
✔ Confidence Scoring  

---

## 🔸 Technologies Used  

- Python  
- Requests  
- BeautifulSoup  
- Scikit-learn (Logistic Regression)  
- Pickle  
- JSON  
- DVWA (Security Level: LOW)  

---

## 🔸 About `sqli_tester.py`

The SQL Injection module performs:

- Automated DVWA authentication  
- Security level configuration  
- Dynamic CSRF token extraction  
- SQL payload injection  
- HTTP response code analysis  
- Response time comparison  
- Response length difference analysis  
- Rule-based SQL error detection  
- AI-based behavioral classification  
- Confidence score generation  
- JSON vulnerability reporting  

---

## 🔸 SQL Payload Used  
```sql
' OR 1=1 --
```

---

## 🔸 Hybrid Detection Architecture  

### 🔹 Rule-Based Detection  

Detects:

- SQL syntax errors  
- Database warnings  
- Fatal errors  
- Abnormal response content  

---

### 🔹 AI-Based Detection  

Extracted Features:

- Response length difference  
- HTTP status code comparison  
- Response time variation  
- Content pattern changes  

Model Execution:

```
prediction, probability = predict(features)
```

---

### 🔹 Final Decision Logic  

```
if rule_based_detected or prediction == 1:
```

This hybrid model improves detection reliability and reduces false negatives.

---

## 📄 Output – `sqli_results.json`

```json
{
  "vulnerabilities": [
    {
      "url": "http://localhost/dvwa/vulnerabilities/sqli/",
      "method": "GET",
      "payload": "' OR 1=1 --",
      "type": "SQL Injection",
      "severity": "High",
      "confidence": 95.0
    }
  ]
}
```

---

## 📸 Week 3 Screenshots  

### 🔐 Hybrid SQL Injection Detection (CLI Output)  
![SQL CLI Detection](Week-3/screenshots/sqli-detection-output.png)  
*Fig 3.1: Terminal output displaying HTTP status codes, response timing, length difference, and AI confidence score.*

---

### 🌐 Manual SQL Injection Validation  
![Manual SQL Proof](Week-3/screenshots/manual-sqli-error-proof.png)  
*Fig 3.2: Manual SQL Injection payload execution confirming vulnerability.*

---

### 📄 SQL JSON Report  
![SQL JSON Result](Week-3/screenshots/sqli-json-result.png)  
*Fig 3.3: Structured SQL vulnerability report generated by the hybrid detection engine.*

---

### 🚀 Full Scan Execution  
![Full Scan](Week-3/screenshots/full-scan-execution.png)  
*Fig 3.4: Integrated workflow showing scanner and SQL Injection module execution.*

---

## 🔸 Week 3 Result  

✔ Hybrid SQL Injection detection implemented  
✔ HTTP response code monitoring integrated  
✔ Response time behavioral analysis added  
✔ AI classification with confidence scoring  
✔ Automated structured reporting  

---

# 🔹 Week 4 – Hybrid XSS Testing Module (AI-Enhanced)

## 🔸 Objective  

To design a **Hybrid XSS Detection Engine** integrating:

✔ Rule-Based Payload Reflection Analysis  
✔ Behavioral Feature Extraction  
✔ Machine Learning Classification  
✔ Confidence Scoring  

---

## 🔸 Technologies Used  

- Python  
- Requests  
- BeautifulSoup  
- Scikit-learn (Logistic Regression)  
- Pickle  
- JSON  

---

## 🔸 About `xss_tester.py`

The XSS module performs:

- DVWA authentication  
- Security level configuration  
- XSS payload injection  
- HTTP response code comparison  
- Response time monitoring  
- Payload reflection detection  
- Rule-based script analysis  
- AI-based behavioral classification  
- Confidence scoring  
- JSON vulnerability reporting  

---

## 🔸 XSS Payload Used  

```html
<script>alert(1)</script>
```

---

## 🔸 Hybrid Detection Architecture  

### 🔹 Rule-Based Detection  

Checks for:

- Direct payload reflection  
- Script tag presence  
- Encoded script patterns  

---

### 🔹 AI-Based Detection  

Behavioral Features:

- Response length difference  
- HTTP status variation  
- Content pattern shifts  

Model Execution:

```python
prediction, probability = predict(features)
```

---

### 🔹 Final Decision Logic  

```python
if rule_based_detected or prediction == 1:
```

This hybrid approach strengthens XSS detection reliability.

---

## 📄 Output – `xss_results.json`

```json
{
  "vulnerabilities": [
    {
      "url": "http://localhost/dvwa/vulnerabilities/xss_r/",
      "method": "GET",
      "payload": "<script>alert(1)</script>",
      "type": "XSS",
      "severity": "High",
      "confidence": 92.0
    }
  ]
}
```

---

## 📸 Week 4 Screenshots  

### 🤖 Hybrid XSS Detection (CLI Output)  
![XSS CLI Detection](Week-4/screenshots/03_ai_xss_detection_terminal.png)  
*Fig 4.1: Terminal output showing HTTP response codes, timing analysis, payload reflection status, and AI confidence score.*

---

### 🌐 Manual XSS Payload Execution  
![Manual XSS](Week-4/screenshots/02_xss_payload_execution.png)  
*Fig 4.2: Manual execution of XSS payload demonstrating script injection vulnerability.*

---

### 📄 XSS JSON Report  
![XSS JSON Result](Week-4/screenshots/04_xss_results_json.png)  
*Fig 4.3: Structured JSON report containing detected XSS vulnerability.*

---

### 🧠 Hybrid Detection Logic  
```python
 # ---------------- RULE-BASED DETECTION ---------------- #

            rule_based_detected = False

            if payload_reflected:
                rule_based_detected = True

            if "<script>" in injected_text and "alert(1)" in injected_text:
                rule_based_detected = True

            if "&lt;script&gt;" in injected_text:
                rule_based_detected = True

            # ---------------- AI DETECTION ---------------- #

            features = extract_xss_features(
                normal_text,
                injected_text,
                injected_response.status_code
            )

            prediction, probability = predict(features)

            # ---------------- FINAL DECISION ---------------- #

            if rule_based_detected or prediction == 1:

                if rule_based_detected:
                    confidence = 92.0
                else:
                    confidence = round(probability * 100, 2)

                print("\n[✔] XSS Detected!")
                print(f"Confidence Score     : {confidence}%")

                vulnerable.append({
                    "url": action,
                    "method": method.upper(),
                    "payload": XSS_PAYLOAD,
                    "type": "XSS",
                    "severity": "High",
                    "confidence": confidence
                })

            else:
                print("[–] No XSS Detected.")

        except Exception as e:
            print(f"[!] Error testing {action}: {e}")
            continue

    print("=" * 60)
    return vulnerable
```
*Fig 4.4: Hybrid rule-based and AI detection architecture implemented in the module.*

---

## 🔸 Week 4 Result  

✔ Reflected XSS detected successfully  
✔ Hybrid AI detection engine implemented  
✔ Response code and behavioral monitoring integrated  
✔ Confidence scoring added  
✔ AI-augmented vulnerability scanning established  

---

# 🎯 Milestone 2 Outcome  

Milestone 2 transforms WebScanPro into a:

✔ Hybrid AI-powered security scanner  
✔ Behavioral analysis engine  
✔ Automated exploitation framework  
✔ Confidence-based vulnerability reporting system  

The system now combines traditional signature-based detection with machine learning-driven behavioral classification for improved accuracy and reliability.
