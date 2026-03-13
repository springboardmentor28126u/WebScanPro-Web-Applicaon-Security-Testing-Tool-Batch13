# WebScanPro-Web-Applicaon-Security-Testing-Tool-Batch13
# Web Application Security Testing Lab – DVWA (Week 1)

## 📌 Project Overview

This project focuses on learning **Web Application Security Testing** using **DVWA (Damn Vulnerable Web Application)**. DVWA is an intentionally vulnerable web application designed to help beginners understand common web security vulnerabilities in a safe environment.

In this project, DVWA is installed and run using **Docker**, which allows us to create an isolated local lab without installing complex server software manually.

### Objectives

* Create a local security testing lab using Docker
* Install and run DVWA successfully
* Understand how vulnerable web applications work
* Explore common web security flaws
* Prepare for advanced penetration testing in future stages

### Tools Used

* Docker Desktop
* DVWA (Damn Vulnerable Web Application)
* Web Browser (Chrome/Firefox)

---

## ⚙️ Installation and Setup

### Step 1: Verify Docker Installation

Make sure Docker Desktop is running.

Open Command Prompt or Terminal and run:

```
docker --version
```

If a version number appears, Docker is installed correctly.

---

### Step 2: Download DVWA Docker Image

Run the following command to download DVWA:

```
docker pull vulnerables/web-dvwa
```
<img width="1260" height="738" alt="image" src="https://github.com/user-attachments/assets/5747d43d-9993-4267-8d4a-0ff645dd3f5b" />

This downloads DVWA and all required dependencies.

---

### Step 3: Run DVWA Container

Start DVWA using:

```
docker run -d -p 8080:80 vulnerables/web-dvwa
```

Explanation:

* `-d` → Runs container in background
* `-p 8080:80` → Maps DVWA to port 8080

---

### Step 4: Access DVWA

Open your browser and go to:

```
http://localhost:8080
```

Login credentials:

* **Username:** admin
* **Password:** password
* <img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/92c76df0-883d-4d99-899b-ecee58e4b133" />


After login, click **Create/Reset Database**.

DVWA is now ready to use.

---

## 🔍 Manual Exploration of DVWA

### Step 1: Dashboard Overview

After login, explore the DVWA dashboard. It contains multiple vulnerability modules available in the left navigation menu.

---


### Step 2: Set Security Level

Go to **DVWA Security** and set the level to:

```
Low
```
<img width="917" height="679" alt="image" src="https://github.com/user-attachments/assets/517e139b-710a-4d03-8e54-5a0143dd015c" />

This makes vulnerabilities easier to understand for beginners.

---

### Step 3: Explore Vulnerability Modules

DVWA includes modules such as:

* SQL Injection
* Cross-Site Scripting (XSS)
* Command Injection
* File Upload
* Brute Force Attacks
* <img width="1030" height="609" alt="image" src="https://github.com/user-attachments/assets/9ab22d3a-caa7-418c-961b-3ace7223398c" />


For each module:

1. Read the instructions provided
2. Enter sample inputs
3. Observe system behavior

---

### Step 4: Docker Container Management

View running containers:

```
docker ps
```

Stop DVWA:

```
docker stop <container_id>
```

Restart DVWA:

```
docker start <container_id>
```

---

### Step 5: Observe Security Flaws

While testing DVWA, pay attention to:

* Weak input validation
* Poor authentication mechanisms
* Insecure database queries
* Improper error handling

These simulate real-world vulnerabilities.

---

## ⚠️ Ethical Use Policy

This lab is strictly for **educational purposes only**.

Do not attempt to exploit real websites without permission. Always follow ethical hacking guidelines.

---

## ✅ Conclusion

By completing Week 1, we successfully:

* Installed DVWA using Docker
* Created a safe local testing lab
* Explored DVWA modules
* Learned about common web vulnerabilities

This setup forms the foundation for advanced web security testing in upcoming project phases.

---

## 🚀 Next Steps

Future work includes:

* Vulnerability scanning
* Penetration testing
* Security analysis
* Documentation and reporting

---

You said:
# Week 2: Target Scanning Module – Project Documentation

## Objective

The objective of Week 2 was to build a **Target Scanning Module** that automatically scans a web application and collects important information such as:

* Web pages and links
* Forms and input fields
* Interactive elements for security testing

This module helps prepare the target system for vulnerability analysis in later stages.

---

## Tools Used

The following tools and libraries were used:

* **Python** – Programming language used to build the crawler
* **Requests Library** – To send HTTP requests and fetch webpage content
* **BeautifulSoup** – To parse HTML and extract links and forms
* **JSON** – To store structured scan results

---

## Implementation

A Python-based crawler (crawler.py) was developed to scan the DVWA web application running on localhost.

### Key Features of the Crawler

The crawler performs the following tasks:

1. Sends a request to the target URL
2. Extracts all hyperlinks from the webpage
3. Detects HTML forms and their input fields
4. Structures the collected data
5. Saves results in a JSON file

---

## Crawler Code

python
import requests
from bs4 import BeautifulSoup
import json

TARGET_URL = "http://localhost:8080"

def crawl_website(url):
    print("Crawling:", url)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href:
            full_link = requests.compat.urljoin(url, href)
            links.append(full_link)

    forms = []
    for form in soup.find_all("form"):
        form_data = {
            "action": form.get("action"),
            "method": form.get("method"),
            "inputs": []
        }

        for input_tag in form.find_all("input"):
            input_info = {
                "name": input_tag.get("name"),
                "type": input_tag.get("type")
            }
            form_data["inputs"].append(input_info)

        forms.append(form_data)

    results = {
        "target_url": url,
        "total_links_found": len(links),
        "links": links,
        "forms": forms
    }

    with open("scan_results.json", "w") as file:
        json.dump(results, file, indent=4)

    print("Crawling completed!")

crawl_website(TARGET_URL)


---

## Output and Data Storage

The crawler generates a file named:

**scan_results.json**

This file is stored in the crawler project folder and contains:

* Total number of discovered links
* List of URLs
* Forms and input structures
* Metadata required for future testing modules

This structured data will be used in upcoming modules to automate vulnerability scanning.

---

## Results

The crawler successfully scanned the DVWA web application and extracted:

* Multiple internal navigation links
* Login and input forms
* Form input fields

The data was saved in structured JSON format for easy reuse.

---

## Conclusion

The Week 2 Target Scanning Module successfully implemented an automated crawler that:

* Discovers webpages and interactive elements
* Organizes target metadata
* Prepares the system for vulnerability testing
* # 📘 Week 3 – SQL Injection Testing and Verification Module

---

## 📌 Introduction

In Week 3, SQL Injection testing was performed on **DVWA (Damn Vulnerable Web Application)** to analyze how vulnerable web applications behave under malicious input and how increasing security configurations prevents such attacks.

This module focuses on **practical vulnerability identification and security verification**.

---

## 🎯 Objectives

- Understand SQL Injection vulnerability
- Test SQL Injection at **Low** security level
- Verify vulnerability behavior
- Test prevention at **High** security level
- Compare vulnerable and secure configurations

---

## 🛠️ Tools Used

| Tool | Purpose |
|------|---------|
| DVWA (Damn Vulnerable Web Application) | Target vulnerable web app |
| Google Chrome Browser | Interface for testing |
| Localhost Testing Environment | Isolated lab environment |

---

## 🧪 SQL Injection Payload Used
```sql
' OR '1'='1
```

This payload exploits weak input handling by injecting a condition that always evaluates to `TRUE`, bypassing the intended query logic.

---
<img width="660" height="106" alt="image" src="https://github.com/user-attachments/assets/4f7b504a-af3d-4e1c-b669-3e656c2cb269" />

## 🔬 Procedure

### Phase 1: Low Security Testing

1. Logged into DVWA
2. Navigated to the **SQL Injection** module
3. Set security level to **Low**
4. Entered a valid input — observed normal behavior
5. Entered malicious payload `' OR '1'='1` — observed results
6. <img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/857c9613-5fa7-4145-8c93-1707a23041ec" />


### Phase 2: High Security Testing

1. Changed security level to **High**
2. Re-entered the same malicious payload
3. Observed system behavior and compared results
<img width="1299" height="728" alt="image" src="https://github.com/user-attachments/assets/fffbb06e-c326-4048-8d51-faac1add6be6" />

---

## 🔎 Observations

### 🔴 Low Security — Vulnerable

- The application returned **all user records**
- Malicious input was directly appended to the SQL query
- No input validation was applied
- The condition `'1'='1'` evaluated to `TRUE`
- The `WHERE` clause became logically TRUE for all rows
- Authentication and data filtering were **bypassed**
- Sensitive information was **exposed**

### 🟢 High Security — Protected

- The application did **NOT** return all records
- The malicious payload was treated as **normal text**
- Query logic was **not altered**
- Authentication bypass did **not** occur
- Input was properly handled and sanitized
- Security mechanisms **successfully prevented** SQL Injection

---

## 📊 Results

| Metric | Result |
|--------|--------|
| SQL Injection at Low Security | ✅ Successful (Attack worked) |
| Application status at Low | ❌ Vulnerable |
| SQL Injection at High Security | ❌ Failed (Attack blocked) |
| Application status at High | ✅ Secure |

---

## 📈 Comparison: Low vs High Security

| Feature | 🔴 Low Security | 🟢 High Security |
|---------|----------------|-----------------|
| Input Validation | Not Applied | Applied |
| SQL Injection Success | ✅ Yes | ❌ No |
| Authentication Bypass | Possible | Not Possible |
| Data Exposure | All Records Exposed | No Exposure |
| Application Status | **Vulnerable** | **Secure** |

---

## 📚 Learning Outcomes

- Understood how SQL Injection manipulates database queries
- Observed authentication bypass in vulnerable systems
- Learned the importance of **input validation**
- Understood the difference between insecure and secure implementations
- Gained practical experience in vulnerability testing

---

## ✅ Conclusion

The Week 3 SQL Injection Testing module successfully demonstrated how **insecure input handling** can lead to severe security vulnerabilities.

At **Low security level**, the application was vulnerable — allowing authentication bypass and data exposure. The malicious SQL payload altered the query logic and returned all records.

After increasing the security level to **High**, the same attack failed. The system handled the input securely and prevented query manipulation.

> This experiment confirms that **proper input validation** and **secure query handling mechanisms** are essential to protect web applications from SQL Injection attacks.

---

## 📁 Module Info

- **Module:** Week 3 — SQL Injection Testing
- **Platform:** DVWA (Damn Vulnerable Web Application)
- **Environment:** Localhost
- **Security Levels Tested:** Low, High
- # 📘 Week 4 – XSS (Cross-Site Scripting) Testing Module

---

## 📌 Introduction

In Week 4, Cross-Site Scripting (XSS) testing was performed on **DVWA (Damn Vulnerable Web Application)** to analyze how vulnerable web applications behave when malicious JavaScript payloads are injected into form fields and URLs.

This module focuses on **two types of XSS attacks** — Reflected and Stored — and how increasing security configurations prevents such attacks.

---

## 🎯 Objectives

- To understand XSS (Cross-Site Scripting) vulnerability
- To inject JavaScript-based XSS payloads into form fields and URLs
- To detect Reflected and Stored XSS via response analysis
- To test prevention at High security level
- To record vulnerable endpoints and provide XSS prevention tips
- To compare vulnerable and secure configurations

---

## 🛠️ Tools Used

| Tool | Purpose |
|------|---------|
| DVWA (Damn Vulnerable Web Application) | Target vulnerable web app |
| Google Chrome Browser | Interface for testing |
| Localhost Testing Environment | Isolated lab environment |

---

## 🧪 XSS Payloads Used

### Reflected XSS Payload:
```javascript
<script>alert('XSS')</script>
```
<img width="913" height="678" alt="image" src="https://github.com/user-attachments/assets/286fb957-1249-400d-aeca-0c535b984c04" />
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/73caf790-c227-475f-bb80-5a2b6cea04f6" />


### Stored XSS Payload:
```javascript
<script>alert('Stored XSS')</script>
```
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/015faa2f-ce12-4e0d-96c7-f1d5f6392d27" />


These payloads inject JavaScript into the application. If the app is vulnerable, an **alert popup** appears — confirming the attack was successful.
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/8bfd4060-d90a-461e-84c0-731ae736912e" />

---

## 🔬 Procedure

### Phase 1: Low Security Testing

#### 🔁 Reflected XSS Testing
1. Logged into DVWA
2. Navigated to **XSS (Reflected)** module
3. Set security level to **Low**
4. Entered valid input (name) — observed normal behavior
5. Entered malicious payload `<script>alert('XSS')</script>` in the name field
6. Clicked **Submit**
7. Alert popup appeared → ✅ Attack successful
8. Observed "Hello" message after popup — input was reflected back

#### 💾 Stored XSS Testing
1. Navigated to **XSS (Stored)** module
2. Security level kept at **Low**
3. Entered `Test` in the **Name** field
4. Entered malicious payload `<script>alert('Stored XSS')</script>` in the **Message** field
5. Clicked **Sign Guestbook**
6. Alert popup appeared → ✅ Attack successful
7. Refreshed the page — popup appeared again → ✅ Script stored in database

### Phase 2: High Security Testing

1. Changed security level to **High**
2. Navigated to **XSS (Reflected)** — entered same payload
3. No popup appeared → ✅ Attack blocked
4. Navigated to **XSS (Stored)** — entered same payload
5. No popup appeared → ✅ Attack blocked
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/f083a4a7-aeed-4e04-a031-63b6f311b831" />
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/5e86e036-6f22-4230-b339-258f7abe5911" />

---

## 🔎 Observations

### 🔴 Low Security — Vulnerable

- Application executed the injected JavaScript directly
- Alert popup appeared confirming script execution
- Input was **not validated or sanitized**
- Reflected XSS — script ran immediately on submit
- Stored XSS — script was **saved in database** and ran on every page load
- Every user visiting the page would be affected by Stored XSS
- Authentication and session data could be stolen
- Sensitive information was **exposed**

### 🟢 High Security — Protected

- Application did **NOT** execute the injected JavaScript
- Malicious payload was treated as **plain text**
- Input was properly **validated and sanitized**
- No popup appeared in either Reflected or Stored XSS
- Security mechanisms **successfully prevented** XSS attacks

---

## 📊 Results

| Test | Result |
|------|--------|
| Reflected XSS at Low Security | ✅ Successful (Attack worked) |
| Stored XSS at Low Security | ✅ Successful (Attack worked) |
| Reflected XSS at High Security | ❌ Failed (Attack blocked) |
| Stored XSS at High Security | ❌ Failed (Attack blocked) |

---

## 🗺️ Vulnerable Endpoints

| Endpoint | XSS Type | Payload Used | Vulnerable? |
|----------|----------|-------------|-------------|
| `/dvwa/vulnerabilities/xss_r/?name=` | Reflected | `<script>alert('XSS')</script>` | ✅ Yes (Low) |
| `/dvwa/vulnerabilities/xss_s/` (Message field) | Stored | `<script>alert('Stored XSS')</script>` | ✅ Yes (Low) |

---

## 📈 Comparison: Low vs High Security

| Feature | 🔴 Low Security | 🟢 High Security |
|---------|----------------|-----------------|
| Input Validation | Not Applied | Applied |
| Reflected XSS Success | ✅ Yes | ❌ No |
| Stored XSS Success | ✅ Yes | ❌ No |
| Script Execution | Allowed | Blocked |
| Data Exposure | Possible | Not Possible |
| Application Status | **Vulnerable** | **Secure** |

---

## 📚 Difference: Reflected vs Stored XSS

| Feature | 🔁 Reflected XSS | 💾 Stored XSS |
|---------|-----------------|--------------|
| Script saved in DB? | ❌ No | ✅ Yes |
| Who is affected? | Only the attacker | Every user who visits |
| How long does it last? | One request only | Until removed from DB |
| Danger level | Medium | High |
| Test location in DVWA | XSS (Reflected) | XSS (Stored) |

---

## 🛡️ XSS Prevention Tips

**1. Input Validation**
Never trust user input. Reject or strip dangerous characters like `<`, `>`, `"`, `'`.

**2. Output Encoding**
Convert special characters before displaying:
- `<` → `&lt;`
- `>` → `&gt;`
- `"` → `&quot;`

This prevents the browser from executing input as code.

**3. Content Security Policy (CSP)**
Add a browser-level rule that blocks unauthorized scripts from running on your site.

**4. HTTPOnly Cookies**
Mark session cookies as `HTTPOnly` so JavaScript cannot access or steal them.

**5. Use Security Libraries**
Use trusted libraries like **DOMPurify** or **OWASP AntiSamy** to automatically sanitize user inputs.

---

## 📚 Learning Outcomes

- Understood how XSS attacks inject and execute malicious JavaScript
- Learned the difference between Reflected and Stored XSS
- Observed how Stored XSS persists and affects all users
- Learned the importance of input validation and output encoding
- Understood difference between insecure and secure implementations
- Gained practical experience in XSS vulnerability testing

---

## ✅ Conclusion

The Week 4 XSS Testing module successfully demonstrated how **insecure input handling** allows attackers to inject and execute malicious JavaScript in web applications.

At **Low security level**, both Reflected and Stored XSS attacks were successful. The injected scripts executed in the browser, proving that the application was vulnerable to script injection.

At **High security level**, the same attacks failed. The application properly handled and sanitized inputs, preventing any script execution.

Stored XSS proved to be more dangerous than Reflected XSS as the malicious script was saved in the database and executed every time the page was loaded — affecting all users.

> This experiment confirms that **proper input validation**, **output encoding**, and **secure query handling** are essential to protect web applications from XSS attacks.

---

## 📁 Module Info

- **Module:** Week 4 — XSS Testing
- **Platform:** DVWA (Damn Vulnerable Web Application)
- **Environment:** Localhost
- **XSS Types Tested:** Reflected XSS, Stored XSS
- **Security Levels Tested:** Low, High
- # 📘 Week 5 – Authentication and Session Testing Module

---

## 📌 Introduction

In Week 5, **Authentication and Session Security Testing** was performed on **DVWA (Damn Vulnerable Web Application)** to analyze how web applications handle **login authentication and session management**.

Authentication systems protect user accounts, while session management maintains the user’s logged-in state. If these mechanisms are poorly implemented, attackers can perform attacks such as:

- Brute Force login attacks
- Credential guessing
- Session hijacking
- Session fixation

This module demonstrates how weak authentication mechanisms can expose user accounts and sensitive data.

---

## 🎯 Objectives

- Understand authentication vulnerabilities in web applications  
- Test **Brute Force login attacks** on DVWA  
- Analyze weak authentication mechanisms  
- Observe authentication behavior at **Low and High security levels**  
- Identify session management weaknesses  
- Compare vulnerable and protected authentication systems  

---

## 🛠️ Tools Used

| Tool | Purpose |
|------|---------|
| DVWA (Damn Vulnerable Web Application) | Target vulnerable web application |
| Google Chrome Browser | Testing interface |
| Localhost Environment | Safe testing lab |
| Browser Developer Tools | Inspect session cookies |

---

## 🔐 Authentication Attack Tested

### Brute Force Attack

A **Brute Force Attack** attempts to guess a user's password by trying many possible combinations until the correct password is found.

Example login credentials tested:

Other tested passwords:
123456
admin
password
test123

---

## 🔬 Procedure

### Phase 1: Low Security Testing

1. Logged into DVWA
2. Navigated to **Brute Force** module
3. Set **DVWA Security Level to Low**
4. Entered login credentials manually
5. Attempted multiple password combinations
6. Observed system behavior

#### Observations

- The application allowed **unlimited login attempts**
- No CAPTCHA protection was present
- No account lockout mechanism existed
- The system responded immediately to each login attempt
- Attackers could repeatedly try passwords until successful

This confirms the application is **vulnerable to brute force attacks**.

---

### Phase 2: High Security Testing

1. Changed **DVWA Security Level to High**
2. Repeated the same login attempts
3. Observed system behavior

#### Observations

- Additional security checks were applied
- Login attempts were restricted
- Brute force attacks became more difficult
- Authentication bypass attempts failed

This indicates the application implemented **stronger authentication protections**.

---

## 🍪 Session Cookie Analysis

After successful login, the browser generated a **session cookie** to maintain the logged-in state.

Example cookie:

### Observations

- The session ID uniquely identifies a logged-in user
- If attackers steal this cookie, they may hijack the session
- Secure applications protect cookies using security flags

| Security Feature | Purpose |
|-----------------|---------|
| HttpOnly | Prevents JavaScript from accessing cookies |
| Secure | Ensures cookies are sent only over HTTPS |
| SameSite | Prevents cross-site request attacks |

---

## 🔎 Observations

### 🔴 Low Security — Vulnerable

- Unlimited login attempts allowed
- No CAPTCHA protection
- No account lockout mechanism
- Easy password guessing
- High risk of brute force attack
- Weak authentication controls

### 🟢 High Security — Protected

- Stronger authentication mechanisms applied
- Login attempts restricted
- Brute force attack prevented
- Improved security configuration

---

## 📊 Results

| Test | Result |
|------|--------|
| Brute Force at Low Security | ✅ Successful (Attack possible) |
| Authentication Status at Low | ❌ Vulnerable |
| Brute Force at High Security | ❌ Failed (Attack prevented) |
| Authentication Status at High | ✅ Secure |

---

## 📈 Comparison: Low vs High Security

| Feature | 🔴 Low Security | 🟢 High Security |
|--------|----------------|----------------|
| Login Attempt Limit | ❌ None | ✅ Restricted |
| CAPTCHA Protection | ❌ Not Present | ✅ Present |
| Brute Force Success | ✅ Possible | ❌ Not Possible |
| Authentication Strength | Weak | Strong |
| Application Status | **Vulnerable** | **Secure** |

---

## 🛡️ Authentication Security Best Practices

**1. Strong Password Policy**  
Require complex passwords with letters, numbers, and symbols.

**2. Account Lockout Mechanism**  
Lock the account after multiple failed login attempts.

**3. CAPTCHA Verification**  
Prevent automated login attacks.

**4. Secure Session Management**  
Regenerate session IDs after login and logout.

**5. HTTPS Encryption**  
Encrypt login credentials during transmission.

---

## 📚 Learning Outcomes

- Learned how brute force attacks target login systems  
- Understood the importance of authentication protection  
- Observed how weak login systems allow attackers to guess passwords  
- Learned how security configurations prevent brute force attacks  
- Gained practical experience in authentication testing  

---

## ✅ Conclusion

The Week 5 Authentication Testing module demonstrated how **weak login security can expose user accounts to brute force attacks**.

At **Low security level**, the application allowed unlimited login attempts, making it vulnerable to password guessing attacks.

At **High security level**, additional security controls prevented repeated login attempts and protected the authentication system.

This experiment highlights the importance of **secure authentication mechanisms and proper session management** to protect web applications from unauthorized access.

---

## 📁 Module Info

- **Module:** Week 5 — Authentication and Session Testing  
- **Platform:** DVWA (Damn Vulnerable Web Application)  
- **Environment:** Localhost  
- **Attack Type Tested:** Brute Force Authentication Attack  
- **Security Levels Tested:** Low, High
- # 📘 Week 6 – Access Control and IDOR Testing Module

---

## 📌 Introduction

In Week 6, **Access Control Testing** was performed on **DVWA (Damn Vulnerable Web Application)** to understand how web applications protect sensitive resources from unauthorized users.

Access control ensures that users can only access the data and actions they are permitted to use. If access control is weak, attackers may exploit vulnerabilities such as **Insecure Direct Object Reference (IDOR)**.

An **IDOR vulnerability** occurs when an application exposes internal object identifiers such as **user IDs, file IDs, or account numbers** without verifying whether the current user is authorized to access that resource.

This module demonstrates how attackers can manipulate request parameters to gain unauthorized access to sensitive data.

---

## 🎯 Objectives

- Understand **Access Control vulnerabilities**
- Identify **Insecure Direct Object Reference (IDOR)**
- Test unauthorized access by modifying object identifiers
- Observe application behavior at **Low and High security levels**
- Compare vulnerable and secure access control implementations

---

## 🛠️ Tools Used

| Tool | Purpose |
|------|---------|
| DVWA (Damn Vulnerable Web Application) | Target vulnerable web application |
| Google Chrome Browser | Testing interface |
| Localhost Environment | Safe testing lab |
| Browser Developer Tools | Inspect requests and responses |

---

## 🔓 Vulnerability Tested

### Insecure Direct Object Reference (IDOR)

An IDOR vulnerability occurs when an application allows direct access to objects using user-controlled parameters.

Example request:
http://localhost:8080/vulnerabilities/idor/?id=1
If an attacker changes the parameter value:
?id=2
?id=3
?id=4

and the application displays other users' data, it indicates an **IDOR vulnerability**.

---

## 🔬 Procedure

### Phase 1: Low Security Testing

1. Logged into DVWA  
2. Navigated to the **Access Control / IDOR module**  
3. Set **DVWA Security Level to Low**  
4. Observed the request parameter containing a user ID  
5. Modified the ID value manually in the URL  
6. Sent the request and observed the response  

#### Observations

- The application returned **data belonging to different users**
- No authorization validation was applied
- Direct object identifiers were exposed
- Unauthorized data access was possible

This confirms the application is **vulnerable to IDOR attacks**.

---

### Phase 2: High Security Testing

1. Changed **DVWA Security Level to High**
2. Repeated the same parameter manipulation
3. Observed system behavior

#### Observations

- The application restricted access to unauthorized resources
- Requests for other user IDs were blocked
- Authorization checks were properly implemented

This indicates the application implemented **stronger access control mechanisms**.

---

## 🔎 Observations

### 🔴 Low Security — Vulnerable

- Direct object identifiers exposed
- No authorization checks
- Users could access other users' data
- Sensitive information exposed
- Application vulnerable to IDOR attacks

### 🟢 High Security — Protected

- Authorization checks implemented
- Unauthorized access blocked
- User data properly protected
- Secure access control mechanisms applied

---

## 📊 Results

| Test | Result |
|------|--------|
| IDOR Attack at Low Security | ✅ Successful (Unauthorized access possible) |
| Application Status at Low | ❌ Vulnerable |
| IDOR Attack at High Security | ❌ Failed (Access blocked) |
| Application Status at High | ✅ Secure |

---

## 📈 Comparison: Low vs High Security

| Feature | 🔴 Low Security | 🟢 High Security |
|--------|----------------|----------------|
| Authorization Check | ❌ Not Implemented | ✅ Implemented |
| Direct Object Access | Allowed | Restricted |
| Unauthorized Data Access | ✅ Possible | ❌ Not Possible |
| Sensitive Data Exposure | High Risk | Protected |
| Application Status | **Vulnerable** | **Secure** |

---

## 🛡️ Access Control Security Best Practices

**1. Implement Authorization Checks**  
Verify that the user requesting a resource has permission to access it.

**2. Use Indirect Object References**  
Avoid exposing internal database IDs directly in URLs.

**3. Role-Based Access Control (RBAC)**  
Restrict system functionality based on user roles.

**4. Validate Every Request**  
Each request must verify authorization before returning data.

**5. Monitor Access Logs**  
Track suspicious access attempts to detect attacks.

---

## 📚 Learning Outcomes

- Learned how **access control mechanisms protect sensitive data**
- Understood how **IDOR vulnerabilities allow unauthorized data access**
- Observed the difference between **vulnerable and secure implementations**
- Gained practical experience in **access control testing**
- Learned the importance of **proper authorization checks**

---

## ✅ Conclusion

The Week 6 Access Control Testing module demonstrated how **improper authorization checks can expose sensitive data through IDOR vulnerabilities**.

At **Low security level**, the application allowed direct access to different user records by modifying object identifiers, confirming the presence of an IDOR vulnerability.

At **High security level**, the application implemented proper authorization checks and prevented unauthorized access.

This experiment highlights the importance of **secure access control mechanisms** in protecting web applications from unauthorized data exposure.

---

## 📁 Module Info

- **Module:** Week 6 — Access Control and IDOR Testing  
- **Platform:** DVWA (Damn Vulnerable Web Application)  
- **Environment:** Localhost  
- **Vulnerability Tested:** Insecure Direct Object Reference (IDOR)  
- **Security Levels Tested:** Low, High
