# WebScanPro-Web-Applicaon-Security-Testing-Tool-Batch13


## 📖 Project Overview

WebScanPro is an automated web application security testing tool designed to detect common vulnerabilities such as:

- SQL Injection (SQLi)
- Cross-Site Scripting (XSS)
- Broken Authentication
- Insecure Direct Object Reference (IDOR)
- Other OWASP Top 10 vulnerabilities

The goal of the project is to scan web applications, simulate attack vectors, and generate structured security reports with suggested mitigation techniques.


## 🛠 Environment Setup

### Local Setup Using XAMPP

- Installed **XAMPP (Apache + MySQL)**
- Enabled Apache and MySQL services
- Downloaded and configured **DVWA (Damn Vulnerable Web Application)**
- Verified application at: `http://localhost/dvwa`
- Set security level to **Low** for controlled manual testing

I also explored **OWASP Juice Shop** and **bWAPP** to understand architectural differences, but detailed manual testing was performed on DVWA.

---

##  Exploration of Target Application (DVWA)

### 1️⃣ Structure Analysis

- Backend: PHP
- Database: MySQL
- Server: Apache
- Multiple vulnerability modules available
- User input handled via GET and POST methods
- Direct interaction between user input and database queries

Juice Shop follows a modern Node.js + Angular architecture with API-based communication.  
bWAPP is similar to DVWA and provides categorized vulnerability labs.

---

### 2️⃣ Functionality Analysis

Observed key features:

- Login authentication
- Input forms for data retrieval
- Comment/message submission
- User management modules

Each feature processes user input on the server side, creating potential attack surfaces.

---

##  Manual Testing Process

Before implementing automation, I manually tested vulnerabilities to understand how they behave.

---

### 🔹 SQL Injection (SQLi)

- Entered normal user ID → received expected record.
- Injected payload: `1' OR '1'='1`
- Application returned all user records.

This confirmed:
- User input was directly inserted into SQL queries.
- No proper input validation was implemented.

I also observed SQL error messages, indicating information disclosure.



---

### 🔹 Cross-Site Scripting (XSS)

#### Reflected XSS
- Injected: `<script>alert(1)</script>`
- Browser executed the script immediately.
- Confirmed lack of input sanitization and output encoding.

#### Stored XSS
- Submitted the same payload in the message field.
- Script executed again after page reload.
- Confirmed unsanitized input stored in database.

---

### 🔹 Authentication Weakness

- Verified incorrect credentials were rejected.
- Injected payload in username field:  
  `admin' OR '1'='1`
- Successfully bypassed login without valid password.
- Observed no rate limiting or account lockout.

This indicates:
- SQL Injection-based authentication bypass
- Susceptibility to brute-force attacks

---

### 🔹 Authorization Testing

- Logged in as a non-admin user.
- Confirmed admin modules were hidden from navigation.
- Attempted direct URL access to restricted pages.
- Server blocked access (proper server-side access control observed).

---

