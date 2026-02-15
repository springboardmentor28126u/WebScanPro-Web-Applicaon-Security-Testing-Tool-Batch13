
<div align="center">

# 🚀 WEBSANPRO – WEB APPLICATION SECURITY TESTING TOOL - BATCH 13 🚀

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

```
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

### 🏠 DVWA Dashboard
![DVWA Dashboard](Week-1/screenshots/dvwa-dashboard.png)

### 🔐 Brute Force Module
![Brute Force Page](Week-1/screenshots/dvwa-bruteforce-page.png)

### 💉 SQL Injection Module
![SQL Injection Page](Week-1/screenshots/dvwa-sql-injection-page.png)

### ⚡ XSS Reflected Module
![XSS Reflected Page](Week-1/screenshots/dvwa-xss-reflected-page.png)
  

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

```
{
    "urls": [
        "http://localhost/dvwa/#",
        "http://localhost/dvwa/",
        "http://localhost/dvwa/instructions.php",
        "http://localhost/dvwa/instructions.php#",
        "http://localhost/dvwa/setup.php",
        "http://localhost/dvwa/setup.php#",
        "http://localhost/dvwa/vulnerabilities/brute/",
        "http://localhost/dvwa/vulnerabilities/brute/#",
        "http://localhost/dvwa/vulnerabilities/exec/",
        "http://localhost/dvwa/vulnerabilities/exec/#",
        "http://localhost/dvwa/vulnerabilities/csrf/",
        "http://localhost/dvwa/vulnerabilities/csrf/#",
        "http://localhost/dvwa/vulnerabilities/fi/?page=include.php",
        "http://localhost/dvwa/vulnerabilities/fi/?page=include.php#",
        "http://localhost/dvwa/vulnerabilities/upload/",
        "http://localhost/dvwa/vulnerabilities/upload/#",
        "http://localhost/dvwa/vulnerabilities/captcha/",
        "http://localhost/dvwa/vulnerabilities/captcha/#",
        "http://localhost/dvwa/vulnerabilities/sqli/",
        "http://localhost/dvwa/vulnerabilities/sqli/#",
        "http://localhost/dvwa/vulnerabilities/sqli_blind/",
        "http://localhost/dvwa/vulnerabilities/sqli_blind/#",
        "http://localhost/dvwa/vulnerabilities/weak_id/",
        "http://localhost/dvwa/vulnerabilities/weak_id/#",
        "http://localhost/dvwa/vulnerabilities/xss_d/",
        "http://localhost/dvwa/vulnerabilities/xss_d/#",
        "http://localhost/dvwa/vulnerabilities/xss_r/",
        "http://localhost/dvwa/vulnerabilities/xss_r/#",
        "http://localhost/dvwa/vulnerabilities/xss_s/",
        "http://localhost/dvwa/vulnerabilities/xss_s/#",
        "http://localhost/dvwa/vulnerabilities/csp/",
        "http://localhost/dvwa/vulnerabilities/csp/#",
        "http://localhost/dvwa/vulnerabilities/javascript/",
        "http://localhost/dvwa/vulnerabilities/javascript/#",
        "http://localhost/dvwa/vulnerabilities/authbypass/",
        "http://localhost/dvwa/vulnerabilities/authbypass/#",
        "http://localhost/dvwa/vulnerabilities/open_redirect/",
        "http://localhost/dvwa/vulnerabilities/open_redirect/#",
        "http://localhost/dvwa/vulnerabilities/cryptography/",
        "http://localhost/dvwa/vulnerabilities/cryptography/#",
        "http://localhost/dvwa/vulnerabilities/api/",
        "http://localhost/dvwa/vulnerabilities/api/#",
        "http://localhost/dvwa/security.php",
        "http://localhost/dvwa/security.php#",
        "http://localhost/dvwa/phpinfo.php",
        "http://localhost/dvwa/phpinfo.php#module_apache2handler",
        "http://localhost/dvwa/phpinfo.php#module_bcmath",
        "http://localhost/dvwa/phpinfo.php#module_bz2",
        "http://localhost/dvwa/phpinfo.php#module_calendar",
        "http://localhost/dvwa/phpinfo.php#module_core",
        "http://localhost/dvwa/phpinfo.php#module_ctype",
        "http://localhost/dvwa/phpinfo.php#module_curl",
        "http://localhost/dvwa/phpinfo.php#module_date",
        "http://localhost/dvwa/phpinfo.php#module_dom",
        "http://localhost/dvwa/phpinfo.php#module_exif",
        "http://localhost/dvwa/phpinfo.php#module_fileinfo",
        "http://localhost/dvwa/phpinfo.php#module_filter",
        "http://localhost/dvwa/phpinfo.php#module_ftp",
        "http://localhost/dvwa/phpinfo.php#module_gettext",
        "http://localhost/dvwa/phpinfo.php#module_hash",
        "http://localhost/dvwa/phpinfo.php#module_iconv",
        "http://localhost/dvwa/phpinfo.php#module_json",
        "http://localhost/dvwa/phpinfo.php#module_libxml",
        "http://localhost/dvwa/phpinfo.php#module_mbstring",
        "http://localhost/dvwa/phpinfo.php#module_mysqli",
        "http://localhost/dvwa/phpinfo.php#module_mysqlnd",
        "http://localhost/dvwa/phpinfo.php#module_openssl",
        "http://localhost/dvwa/phpinfo.php#module_pcre",
        "http://localhost/dvwa/phpinfo.php#module_pdo",
        "http://localhost/dvwa/phpinfo.php#module_pdo_mysql",
        "http://localhost/dvwa/phpinfo.php#module_pdo_sqlite",
        "http://localhost/dvwa/phpinfo.php#module_phar",
        "http://localhost/dvwa/phpinfo.php#module_random",
        "http://localhost/dvwa/phpinfo.php#module_readline",
        "http://localhost/dvwa/phpinfo.php#module_reflection",
        "http://localhost/dvwa/phpinfo.php#module_session",
        "http://localhost/dvwa/phpinfo.php#module_simplexml",
        "http://localhost/dvwa/phpinfo.php#module_spl",
        "http://localhost/dvwa/phpinfo.php#module_standard",
        "http://localhost/dvwa/phpinfo.php#module_tokenizer",
        "http://localhost/dvwa/phpinfo.php#module_xml",
        "http://localhost/dvwa/phpinfo.php#module_xmlreader",
        "http://localhost/dvwa/phpinfo.php#module_xmlwriter",
        "http://localhost/dvwa/phpinfo.php#module_zlib",
        "http://localhost/dvwa/about.php",
        "http://localhost/dvwa/about.php#",
        "http://localhost/dvwa/logout.php",
        "http://localhost/dvwa/vulnerabilities/bac/log_viewer.php",
        "http://localhost/dvwa/vulnerabilities/open_redirect/source/impossible.php?redirect=1",
        "http://localhost/dvwa/vulnerabilities/open_redirect/source/impossible.php?redirect=2",
        "http://localhost/dvwa/vulnerabilities/fi/?page=file1.php",
        "http://localhost/dvwa/vulnerabilities/fi/?page=file2.php",
        "http://localhost/dvwa/vulnerabilities/fi/?page=file3.php",
        "http://localhost/dvwa/instructions.php?doc=readme",
        "http://localhost/dvwa/instructions.php?doc=readme#",
        "http://localhost/dvwa/instructions.php?doc=PDF",
        "http://localhost/dvwa/instructions.php?doc=PDF#",
        "http://localhost/dvwa/instructions.php?doc=changelog",
        "http://localhost/dvwa/instructions.php?doc=changelog#",
        "http://localhost/dvwa/instructions.php?doc=copying",
        "http://localhost/dvwa/instructions.php?doc=copying#",
        "http://localhost/dvwa/docs/DVWA_v1.3.pdf",
        "http://localhost/dvwa/README.ar.md",
        "http://localhost/dvwa/README.zh.md",
        "http://localhost/dvwa/README.fr.md",
        "http://localhost/dvwa/README.ko.md",
        "http://localhost/dvwa/README.fa.md",
        "http://localhost/dvwa/README.pl.md",
        "http://localhost/dvwa/README.pt.md",
        "http://localhost/dvwa/README.es.md",
        "http://localhost/dvwa/README.tr.md",
        "http://localhost/dvwa/README.id.md",
        "http://localhost/dvwa/README.vi.md",
        "http://localhost/dvwa/README.it.md",
        "http://localhost/dvwa/instructions.php?doc=readme#download",
        "http://localhost/dvwa/instructions.php?doc=readme#i-want-to-run-dvwa-on-a-different-port",
        "http://localhost/dvwa/config/config.inc.php.dist",
        "http://localhost/dvwa/compose.yml",
        "http://localhost/dvwa/instructions.php?doc=readme#php-configuration",
        "http://localhost/dvwa/instructions.php?doc=readme#database-setup",
        "http://localhost/dvwa/instructions.php#download",
        "http://localhost/dvwa/instructions.php#i-want-to-run-dvwa-on-a-different-port",
        "http://localhost/dvwa/instructions.php#php-configuration",
        "http://localhost/dvwa/instructions.php#database-setup"
    ],
    "forms": [
        {
            "page": "http://localhost/dvwa/logout.php",
            "action": "http://localhost/dvwa/login.php",
            "method": "post",
            "inputs": [
                {
                    "name": "username",
                    "type": "text",
                    "value": ""
                },
                {
                    "name": "password",
                    "type": "password",
                    "value": ""
                },
                {
                    "name": "Login",
                    "type": "submit",
                    "value": "Login"
                },
                {
                    "name": "user_token",
                    "type": "hidden",
                    "value": "fac1829dc63df029091924174581b615"
                }
            ]
        },
        {
            "page": "http://localhost/dvwa/security.php#",
            "action": "http://localhost/dvwa/security.php#",
            "method": "post",
            "inputs": [
                {
                    "name": "seclev_submit",
                    "type": "submit",
                    "value": "Submit"
                },
                {
                    "name": "user_token",
                    "type": "hidden",
                    "value": "4447be34f8f38a066bf3333993c3c38a"
                }
            ]
        },
        {
            "page": "http://localhost/dvwa/security.php",
            "action": "http://localhost/dvwa/security.php#",
            "method": "post",
            "inputs": [
                {
                    "name": "seclev_submit",
                    "type": "submit",
                    "value": "Submit"
                },
                {
                    "name": "user_token",
                    "type": "hidden",
                    "value": "cb13cb772057259c1585296b60aa44ec"
                }
            ]
        },
        {
            "page": "http://localhost/dvwa/vulnerabilities/cryptography/#",
            "action": "http://localhost/dvwa/vulnerabilities/cryptography/#",
            "method": "get",
            "inputs": [
                {
                    "name": null,
                    "type": "button",
                    "value": "Submit"
                }
            ]
        },
        {
            "page": "http://localhost/dvwa/vulnerabilities/cryptography/",
            "action": "http://localhost/dvwa/vulnerabilities/cryptography/",
            "method": "get",
            "inputs": [
                {
                    "name": null,
                    "type": "button",
                    "value": "Submit"
                }
            ]
        },
        {
            "page": "http://localhost/dvwa/vulnerabilities/open_redirect/source/impossible.php?redirect=1",
            "action": "http://localhost/dvwa/vulnerabilities/open_redirect/source/login.php",
            "method": "post",
            "inputs": [
                {
                    "name": "username",
                    "type": "text",
                    "value": ""
                },
                {
                    "name": "password",
                    "type": "password",
                    "value": ""
                },
                {
                    "name": "Login",
                    "type": "submit",
                    "value": "Login"
                },
                {
                    "name": "user_token",
                    "type": "hidden",
                    "value": "c8d6f480a1381460043e84bc81291ab0"
                }
            ]
        },
        {
            "page": "http://localhost/dvwa/vulnerabilities/open_redirect/source/impossible.php?redirect=2",
            "action": "http://localhost/dvwa/vulnerabilities/open_redirect/source/login.php",
            "method": "post",
            "inputs": [
                {
                    "name": "username",
                    "type": "text",
                    "value": ""
                },
                {
                    "name": "password",
                    "type": "password",
                    "value": ""
                },
                {
                    "name": "Login",
                    "type": "submit",
                    "value": "Login"
                },
                {
                    "name": "user_token",
                    "type": "hidden",
                    "value": "565f8370be83bbb300454642194b58f7"
                }
            ]
        },
        {
            "page": "http://localhost/dvwa/vulnerabilities/csp/#",
            "action": "http://localhost/dvwa/vulnerabilities/csp/#",
            "method": "post",
            "inputs": [
                {
                    "name": null,
                    "type": "button",
                    "value": "Solve the sum"
                }
            ]
        },
        {
            "page": "http://localhost/dvwa/vulnerabilities/csp/",
            "action": "http://localhost/dvwa/vulnerabilities/csp/",
            "method": "post",
            "inputs": [
                {
                    "name": null,
                    "type": "button",
                    "value": "Solve the sum"
                }
            ]
        },
        {
            "page": "http://localhost/dvwa/vulnerabilities/xss_s/#",
            "action": "http://localhost/dvwa/vulnerabilities/xss_s/#",
            "method": "post",
            "inputs": [
                {
                    "name": "txtName",
                    "type": "text",
                    "value": ""
                },
                {
                    "name": "btnSign",
                    "type": "submit",
                    "value": "Sign Guestbook"
                },
                {
                    "name": "btnClear",
                    "type": "submit",
                    "value": "Clear Guestbook"
                },
                {
                    "name": "user_token",
                    "type": "hidden",
                    "value": "762495a75dc9c1600bb79c49335ee13d"
                }
            ]
        },
        {
            "page": "http://localhost/dvwa/vulnerabilities/xss_s/",
            "action": "http://localhost/dvwa/vulnerabilities/xss_s/",
            "method": "post",
            "inputs": [
                {
                    "name": "txtName",
                    "type": "text",
                    "value": ""
                },
                {
                    "name": "btnSign",
                    "type": "submit",
                    "value": "Sign Guestbook"
                },
                {
                    "name": "btnClear",
                    "type": "submit",
                    "value": "Clear Guestbook"
                },
                {
                    "name": "user_token",
                    "type": "hidden",
                    "value": "75c7d5777269ba2bff5a50968f53db78"
                }
            ]
        },
        {
            "page": "http://localhost/dvwa/vulnerabilities/xss_r/#",
            "action": "http://localhost/dvwa/vulnerabilities/xss_r/#",
            "method": "get",
            "inputs": [
                {
                    "name": "name",
                    "type": "text",
                    "value": ""
                },
                {
                    "name": null,
                    "type": "submit",
                    "value": "Submit"
                },
                {
                    "name": "user_token",
                    "type": "hidden",
                    "value": "9f1587e39ce7cfc66aa2dcce14186a27"
                }
            ]
        },
        {
            "page": "http://localhost/dvwa/vulnerabilities/xss_r/",
            "action": "http://localhost/dvwa/vulnerabilities/xss_r/#",
            "method": "get",
            "inputs": [
                {
                    "name": "name",
                    "type": "text",
                    "value": ""
                },
                {
                    "name": null,
                    "type": "submit",
                    "value": "Submit"
                },
                {
                    "name": "user_token",
                    "type": "hidden",
                    "value": "bbf6b01a406c607f98fe098afd186d33"
                }
            ]
        },
        {
            "page": "http://localhost/dvwa/vulnerabilities/xss_d/#",
            "action": "http://localhost/dvwa/vulnerabilities/xss_d/#",
            "method": "get",
            "inputs": [
                {
                    "name": null,
                    "type": "submit",
                    "value": "Select"
                }
            ]
        },
        {
            "page": "http://localhost/dvwa/vulnerabilities/xss_d/",
            "action": "http://localhost/dvwa/vulnerabilities/xss_d/",
            "method": "get",
            "inputs": [
                {
                    "name": null,
                    "type": "submit",
                    "value": "Select"
                }
            ]
        },
        {
            "page": "http://localhost/dvwa/vulnerabilities/weak_id/#",
            "action": "http://localhost/dvwa/vulnerabilities/weak_id/#",
            "method": "post",
            "inputs": [
                {
                    "name": null,
                    "type": "submit",
                    "value": "Generate"
                }
            ]
        },
        {
            "page": "http://localhost/dvwa/vulnerabilities/weak_id/",
            "action": "http://localhost/dvwa/vulnerabilities/weak_id/",
            "method": "post",
            "inputs": [
                {
                    "name": null,
                    "type": "submit",
                    "value": "Generate"
                }
            ]
        },
        {
            "page": "http://localhost/dvwa/vulnerabilities/sqli_blind/#",
            "action": "http://localhost/dvwa/vulnerabilities/sqli_blind/#",
            "method": "get",
            "inputs": [
                {
                    "name": "id",
                    "type": "text",
                    "value": ""
                },
                {
                    "name": "Submit",
                    "type": "submit",
                    "value": "Submit"
                },
                {
                    "name": "user_token",
                    "type": "hidden",
                    "value": "7a1578585ae31ac8527ffb75e56229aa"
                }
            ]
        },
        {
            "page": "http://localhost/dvwa/vulnerabilities/sqli_blind/",
            "action": "http://localhost/dvwa/vulnerabilities/sqli_blind/#",
            "method": "get",
            "inputs": [
                {
                    "name": "id",
                    "type": "text",
                    "value": ""
                },
                {
                    "name": "Submit",
                    "type": "submit",
                    "value": "Submit"
                },
                {
                    "name": "user_token",
                    "type": "hidden",
                    "value": "af2e3be5613cb9da8099bc6d8a6300d1"
                }
            ]
        },
        {
            "page": "http://localhost/dvwa/vulnerabilities/sqli/#",
            "action": "http://localhost/dvwa/vulnerabilities/sqli/#",
            "method": "get",
            "inputs": [
                {
                    "name": "id",
                    "type": "text",
                    "value": ""
                },
                {
                    "name": "Submit",
                    "type": "submit",
                    "value": "Submit"
                },
                {
                    "name": "user_token",
                    "type": "hidden",
                    "value": "2d44fb575e822bca342856eac70a2aa7"
                }
            ]
        },
        {
            "page": "http://localhost/dvwa/vulnerabilities/sqli/",
            "action": "http://localhost/dvwa/vulnerabilities/sqli/#",
            "method": "get",
            "inputs": [
                {
                    "name": "id",
                    "type": "text",
                    "value": ""
                },
                {
                    "name": "Submit",
                    "type": "submit",
                    "value": "Submit"
                },
                {
                    "name": "user_token",
                    "type": "hidden",
                    "value": "85ad35562b7d5dc6354edfc1fc4a8c01"
                }
            ]
        },
        {
            "page": "http://localhost/dvwa/vulnerabilities/captcha/#",
            "action": "http://localhost/dvwa/vulnerabilities/captcha/#",
            "method": "post",
            "inputs": [
                {
                    "name": "step",
                    "type": "hidden",
                    "value": "1"
                },
                {
                    "name": "password_current",
                    "type": "password",
                    "value": ""
                },
                {
                    "name": "password_new",
                    "type": "password",
                    "value": ""
                },
                {
                    "name": "password_conf",
                    "type": "password",
                    "value": ""
                },
                {
                    "name": "user_token",
                    "type": "hidden",
                    "value": "549089a616c058507e27080a5aeaa76d"
                },
                {
                    "name": "Change",
                    "type": "submit",
                    "value": "Change"
                }
            ]
        },
        {
            "page": "http://localhost/dvwa/vulnerabilities/captcha/",
            "action": "http://localhost/dvwa/vulnerabilities/captcha/#",
            "method": "post",
            "inputs": [
                {
                    "name": "step",
                    "type": "hidden",
                    "value": "1"
                },
                {
                    "name": "password_current",
                    "type": "password",
                    "value": ""
                },
                {
                    "name": "password_new",
                    "type": "password",
                    "value": ""
                },
                {
                    "name": "password_conf",
                    "type": "password",
                    "value": ""
                },
                {
                    "name": "user_token",
                    "type": "hidden",
                    "value": "867c80211bbf5b6e36bbb1346a8ef32a"
                },
                {
                    "name": "Change",
                    "type": "submit",
                    "value": "Change"
                }
            ]
        },
        {
            "page": "http://localhost/dvwa/vulnerabilities/upload/#",
            "action": "http://localhost/dvwa/vulnerabilities/upload/#",
            "method": "post",
            "inputs": [
                {
                    "name": "MAX_FILE_SIZE",
                    "type": "hidden",
                    "value": "100000"
                },
                {
                    "name": "uploaded",
                    "type": "file",
                    "value": ""
                },
                {
                    "name": "Upload",
                    "type": "submit",
                    "value": "Upload"
                },
                {
                    "name": "user_token",
                    "type": "hidden",
                    "value": "e455c4eda27120c95b94f2801ddb621d"
                }
            ]
        },
        {
            "page": "http://localhost/dvwa/vulnerabilities/upload/",
            "action": "http://localhost/dvwa/vulnerabilities/upload/#",
            "method": "post",
            "inputs": [
                {
                    "name": "MAX_FILE_SIZE",
                    "type": "hidden",
                    "value": "100000"
                },
                {
                    "name": "uploaded",
                    "type": "file",
                    "value": ""
                },
                {
                    "name": "Upload",
                    "type": "submit",
                    "value": "Upload"
                },
                {
                    "name": "user_token",
                    "type": "hidden",
                    "value": "0c667a98e1e65cbb1fea4ec6c60bfa59"
                }
            ]
        },
        {
            "page": "http://localhost/dvwa/vulnerabilities/fi/?page=file1.php",
            "action": "http://localhost/dvwa/vulnerabilities/fi/login.php",
            "method": "post",
            "inputs": [
                {
                    "name": "username",
                    "type": "text",
                    "value": ""
                },
                {
                    "name": "password",
                    "type": "password",
                    "value": ""
                },
                {
                    "name": "Login",
                    "type": "submit",
                    "value": "Login"
                },
                {
                    "name": "user_token",
                    "type": "hidden",
                    "value": "437efbcd7d74fef6f581886584f534d4"
                }
            ]
        },
        {
            "page": "http://localhost/dvwa/vulnerabilities/fi/?page=file2.php",
            "action": "http://localhost/dvwa/vulnerabilities/fi/login.php",
            "method": "post",
            "inputs": [
                {
                    "name": "username",
                    "type": "text",
                    "value": ""
                },
                {
                    "name": "password",
                    "type": "password",
                    "value": ""
                },
                {
                    "name": "Login",
                    "type": "submit",
                    "value": "Login"
                },
                {
                    "name": "user_token",
                    "type": "hidden",
                    "value": "8c0e8e1f09d3d733576f9e1228257dd0"
                }
            ]
        },
        {
            "page": "http://localhost/dvwa/vulnerabilities/fi/?page=file3.php",
            "action": "http://localhost/dvwa/vulnerabilities/fi/login.php",
            "method": "post",
            "inputs": [
                {
                    "name": "username",
                    "type": "text",
                    "value": ""
                },
                {
                    "name": "password",
                    "type": "password",
                    "value": ""
                },
                {
                    "name": "Login",
                    "type": "submit",
                    "value": "Login"
                },
                {
                    "name": "user_token",
                    "type": "hidden",
                    "value": "46b69cb66dc5a4c47224695d7716dcd5"
                }
            ]
        },
        {
            "page": "http://localhost/dvwa/vulnerabilities/csrf/#",
            "action": "http://localhost/dvwa/vulnerabilities/csrf/#",
            "method": "get",
            "inputs": [
                {
                    "name": "password_current",
                    "type": "password",
                    "value": ""
                },
                {
                    "name": "password_new",
                    "type": "password",
                    "value": ""
                },
                {
                    "name": "password_conf",
                    "type": "password",
                    "value": ""
                },
                {
                    "name": "Change",
                    "type": "submit",
                    "value": "Change"
                },
                {
                    "name": "user_token",
                    "type": "hidden",
                    "value": "05c11f434a46541aa7e1600d7dff12c8"
                }
            ]
        },
        {
            "page": "http://localhost/dvwa/vulnerabilities/csrf/",
            "action": "http://localhost/dvwa/vulnerabilities/csrf/#",
            "method": "get",
            "inputs": [
                {
                    "name": "password_current",
                    "type": "password",
                    "value": ""
                },
                {
                    "name": "password_new",
                    "type": "password",
                    "value": ""
                },
                {
                    "name": "password_conf",
                    "type": "password",
                    "value": ""
                },
                {
                    "name": "Change",
                    "type": "submit",
                    "value": "Change"
                },
                {
                    "name": "user_token",
                    "type": "hidden",
                    "value": "4733db826fbff1584e8e69cf83409d36"
                }
            ]
        },
        {
            "page": "http://localhost/dvwa/vulnerabilities/exec/#",
            "action": "http://localhost/dvwa/vulnerabilities/exec/#",
            "method": "post",
            "inputs": [
                {
                    "name": "ip",
                    "type": "text",
                    "value": ""
                },
                {
                    "name": "Submit",
                    "type": "submit",
                    "value": "Submit"
                },
                {
                    "name": "user_token",
                    "type": "hidden",
                    "value": "b0e73cf92c84bf93b61499d034b28948"
                }
            ]
        },
        {
            "page": "http://localhost/dvwa/vulnerabilities/exec/",
            "action": "http://localhost/dvwa/vulnerabilities/exec/#",
            "method": "post",
            "inputs": [
                {
                    "name": "ip",
                    "type": "text",
                    "value": ""
                },
                {
                    "name": "Submit",
                    "type": "submit",
                    "value": "Submit"
                },
                {
                    "name": "user_token",
                    "type": "hidden",
                    "value": "59ff771b0ec79b837841daa3e72e3b9b"
                }
            ]
        },
        {
            "page": "http://localhost/dvwa/vulnerabilities/brute/#",
            "action": "http://localhost/dvwa/vulnerabilities/brute/#",
            "method": "post",
            "inputs": [
                {
                    "name": "username",
                    "type": "text",
                    "value": ""
                },
                {
                    "name": "password",
                    "type": "password",
                    "value": ""
                },
                {
                    "name": "Login",
                    "type": "submit",
                    "value": "Login"
                },
                {
                    "name": "user_token",
                    "type": "hidden",
                    "value": "1428c9a05c126a6c62bf3fa7195a6d9b"
                }
            ]
        },
        {
            "page": "http://localhost/dvwa/vulnerabilities/brute/",
            "action": "http://localhost/dvwa/vulnerabilities/brute/#",
            "method": "post",
            "inputs": [
                {
                    "name": "username",
                    "type": "text",
                    "value": ""
                },
                {
                    "name": "password",
                    "type": "password",
                    "value": ""
                },
                {
                    "name": "Login",
                    "type": "submit",
                    "value": "Login"
                },
                {
                    "name": "user_token",
                    "type": "hidden",
                    "value": "9210ed454fdd53aaecdb23df58a972a1"
                }
            ]
        },
        {
            "page": "http://localhost/dvwa/setup.php#",
            "action": "http://localhost/dvwa/setup.php#",
            "method": "post",
            "inputs": [
                {
                    "name": "create_db",
                    "type": "submit",
                    "value": "Create / Reset Database"
                },
                {
                    "name": "user_token",
                    "type": "hidden",
                    "value": "d4102b4cf1b3257732ddd5ef70aa84bd"
                }
            ]
        },
        {
            "page": "http://localhost/dvwa/setup.php",
            "action": "http://localhost/dvwa/setup.php#",
            "method": "post",
            "inputs": [
                {
                    "name": "create_db",
                    "type": "submit",
                    "value": "Create / Reset Database"
                },
                {
                    "name": "user_token",
                    "type": "hidden",
                    "value": "a99a5b715e19d2ca0eaeb2562374c210"
                }
            ]
        }
    ]
}
```

---

### 📄 output.txt  

Readable scan summary for quick analysis.

### 📄 Output TXT Result  
```
=== Discovered URLs ===
http://localhost/dvwa/#
http://localhost/dvwa/
http://localhost/dvwa/instructions.php
http://localhost/dvwa/instructions.php#
http://localhost/dvwa/setup.php
http://localhost/dvwa/setup.php#
http://localhost/dvwa/vulnerabilities/brute/
http://localhost/dvwa/vulnerabilities/brute/#
http://localhost/dvwa/vulnerabilities/exec/
http://localhost/dvwa/vulnerabilities/exec/#
http://localhost/dvwa/vulnerabilities/csrf/
http://localhost/dvwa/vulnerabilities/csrf/#
http://localhost/dvwa/vulnerabilities/fi/?page=include.php
http://localhost/dvwa/vulnerabilities/fi/?page=include.php#
http://localhost/dvwa/vulnerabilities/upload/
http://localhost/dvwa/vulnerabilities/upload/#
http://localhost/dvwa/vulnerabilities/captcha/
http://localhost/dvwa/vulnerabilities/captcha/#
http://localhost/dvwa/vulnerabilities/sqli/
http://localhost/dvwa/vulnerabilities/sqli/#
http://localhost/dvwa/vulnerabilities/sqli_blind/
http://localhost/dvwa/vulnerabilities/sqli_blind/#
http://localhost/dvwa/vulnerabilities/weak_id/
http://localhost/dvwa/vulnerabilities/weak_id/#
http://localhost/dvwa/vulnerabilities/xss_d/
http://localhost/dvwa/vulnerabilities/xss_d/#
http://localhost/dvwa/vulnerabilities/xss_r/
http://localhost/dvwa/vulnerabilities/xss_r/#
http://localhost/dvwa/vulnerabilities/xss_s/
http://localhost/dvwa/vulnerabilities/xss_s/#
http://localhost/dvwa/vulnerabilities/csp/
http://localhost/dvwa/vulnerabilities/csp/#
http://localhost/dvwa/vulnerabilities/javascript/
http://localhost/dvwa/vulnerabilities/javascript/#
http://localhost/dvwa/vulnerabilities/authbypass/
http://localhost/dvwa/vulnerabilities/authbypass/#
http://localhost/dvwa/vulnerabilities/open_redirect/
http://localhost/dvwa/vulnerabilities/open_redirect/#
http://localhost/dvwa/vulnerabilities/cryptography/
http://localhost/dvwa/vulnerabilities/cryptography/#
http://localhost/dvwa/vulnerabilities/api/
http://localhost/dvwa/vulnerabilities/api/#
http://localhost/dvwa/security.php
http://localhost/dvwa/security.php#
http://localhost/dvwa/phpinfo.php
http://localhost/dvwa/phpinfo.php#module_apache2handler
http://localhost/dvwa/phpinfo.php#module_bcmath
http://localhost/dvwa/phpinfo.php#module_bz2
http://localhost/dvwa/phpinfo.php#module_calendar
http://localhost/dvwa/phpinfo.php#module_core
http://localhost/dvwa/phpinfo.php#module_ctype
http://localhost/dvwa/phpinfo.php#module_curl
http://localhost/dvwa/phpinfo.php#module_date
http://localhost/dvwa/phpinfo.php#module_dom
http://localhost/dvwa/phpinfo.php#module_exif
http://localhost/dvwa/phpinfo.php#module_fileinfo
http://localhost/dvwa/phpinfo.php#module_filter
http://localhost/dvwa/phpinfo.php#module_ftp
http://localhost/dvwa/phpinfo.php#module_gettext
http://localhost/dvwa/phpinfo.php#module_hash
http://localhost/dvwa/phpinfo.php#module_iconv
http://localhost/dvwa/phpinfo.php#module_json
http://localhost/dvwa/phpinfo.php#module_libxml
http://localhost/dvwa/phpinfo.php#module_mbstring
http://localhost/dvwa/phpinfo.php#module_mysqli
http://localhost/dvwa/phpinfo.php#module_mysqlnd
http://localhost/dvwa/phpinfo.php#module_openssl
http://localhost/dvwa/phpinfo.php#module_pcre
http://localhost/dvwa/phpinfo.php#module_pdo
http://localhost/dvwa/phpinfo.php#module_pdo_mysql
http://localhost/dvwa/phpinfo.php#module_pdo_sqlite
http://localhost/dvwa/phpinfo.php#module_phar
http://localhost/dvwa/phpinfo.php#module_random
http://localhost/dvwa/phpinfo.php#module_readline
http://localhost/dvwa/phpinfo.php#module_reflection
http://localhost/dvwa/phpinfo.php#module_session
http://localhost/dvwa/phpinfo.php#module_simplexml
http://localhost/dvwa/phpinfo.php#module_spl
http://localhost/dvwa/phpinfo.php#module_standard
http://localhost/dvwa/phpinfo.php#module_tokenizer
http://localhost/dvwa/phpinfo.php#module_xml
http://localhost/dvwa/phpinfo.php#module_xmlreader
http://localhost/dvwa/phpinfo.php#module_xmlwriter
http://localhost/dvwa/phpinfo.php#module_zlib
http://localhost/dvwa/about.php
http://localhost/dvwa/about.php#
http://localhost/dvwa/logout.php
http://localhost/dvwa/vulnerabilities/bac/log_viewer.php
http://localhost/dvwa/vulnerabilities/open_redirect/source/impossible.php?redirect=1
http://localhost/dvwa/vulnerabilities/open_redirect/source/impossible.php?redirect=2
http://localhost/dvwa/vulnerabilities/fi/?page=file1.php
http://localhost/dvwa/vulnerabilities/fi/?page=file2.php
http://localhost/dvwa/vulnerabilities/fi/?page=file3.php
http://localhost/dvwa/instructions.php?doc=readme
http://localhost/dvwa/instructions.php?doc=readme#
http://localhost/dvwa/instructions.php?doc=PDF
http://localhost/dvwa/instructions.php?doc=PDF#
http://localhost/dvwa/instructions.php?doc=changelog
http://localhost/dvwa/instructions.php?doc=changelog#
http://localhost/dvwa/instructions.php?doc=copying
http://localhost/dvwa/instructions.php?doc=copying#
http://localhost/dvwa/docs/DVWA_v1.3.pdf
http://localhost/dvwa/README.ar.md
http://localhost/dvwa/README.zh.md
http://localhost/dvwa/README.fr.md
http://localhost/dvwa/README.ko.md
http://localhost/dvwa/README.fa.md
http://localhost/dvwa/README.pl.md
http://localhost/dvwa/README.pt.md
http://localhost/dvwa/README.es.md
http://localhost/dvwa/README.tr.md
http://localhost/dvwa/README.id.md
http://localhost/dvwa/README.vi.md
http://localhost/dvwa/README.it.md
http://localhost/dvwa/instructions.php?doc=readme#download
http://localhost/dvwa/instructions.php?doc=readme#i-want-to-run-dvwa-on-a-different-port
http://localhost/dvwa/config/config.inc.php.dist
http://localhost/dvwa/compose.yml
http://localhost/dvwa/instructions.php?doc=readme#php-configuration
http://localhost/dvwa/instructions.php?doc=readme#database-setup
http://localhost/dvwa/instructions.php#download
http://localhost/dvwa/instructions.php#i-want-to-run-dvwa-on-a-different-port
http://localhost/dvwa/instructions.php#php-configuration
http://localhost/dvwa/instructions.php#database-setup

=== Forms & Input Fields ===
{'page': 'http://localhost/dvwa/logout.php', 'action': 'http://localhost/dvwa/login.php', 'method': 'post', 'inputs': [{'name': 'username', 'type': 'text', 'value': ''}, {'name': 'password', 'type': 'password', 'value': ''}, {'name': 'Login', 'type': 'submit', 'value': 'Login'}, {'name': 'user_token', 'type': 'hidden', 'value': 'fac1829dc63df029091924174581b615'}]}
{'page': 'http://localhost/dvwa/security.php#', 'action': 'http://localhost/dvwa/security.php#', 'method': 'post', 'inputs': [{'name': 'seclev_submit', 'type': 'submit', 'value': 'Submit'}, {'name': 'user_token', 'type': 'hidden', 'value': '4447be34f8f38a066bf3333993c3c38a'}]}
{'page': 'http://localhost/dvwa/security.php', 'action': 'http://localhost/dvwa/security.php#', 'method': 'post', 'inputs': [{'name': 'seclev_submit', 'type': 'submit', 'value': 'Submit'}, {'name': 'user_token', 'type': 'hidden', 'value': 'cb13cb772057259c1585296b60aa44ec'}]}
{'page': 'http://localhost/dvwa/vulnerabilities/cryptography/#', 'action': 'http://localhost/dvwa/vulnerabilities/cryptography/#', 'method': 'get', 'inputs': [{'name': None, 'type': 'button', 'value': 'Submit'}]}
{'page': 'http://localhost/dvwa/vulnerabilities/cryptography/', 'action': 'http://localhost/dvwa/vulnerabilities/cryptography/', 'method': 'get', 'inputs': [{'name': None, 'type': 'button', 'value': 'Submit'}]}
{'page': 'http://localhost/dvwa/vulnerabilities/open_redirect/source/impossible.php?redirect=1', 'action': 'http://localhost/dvwa/vulnerabilities/open_redirect/source/login.php', 'method': 'post', 'inputs': [{'name': 'username', 'type': 'text', 'value': ''}, {'name': 'password', 'type': 'password', 'value': ''}, {'name': 'Login', 'type': 'submit', 'value': 'Login'}, {'name': 'user_token', 'type': 'hidden', 'value': 'c8d6f480a1381460043e84bc81291ab0'}]}
{'page': 'http://localhost/dvwa/vulnerabilities/open_redirect/source/impossible.php?redirect=2', 'action': 'http://localhost/dvwa/vulnerabilities/open_redirect/source/login.php', 'method': 'post', 'inputs': [{'name': 'username', 'type': 'text', 'value': ''}, {'name': 'password', 'type': 'password', 'value': ''}, {'name': 'Login', 'type': 'submit', 'value': 'Login'}, {'name': 'user_token', 'type': 'hidden', 'value': '565f8370be83bbb300454642194b58f7'}]}
{'page': 'http://localhost/dvwa/vulnerabilities/csp/#', 'action': 'http://localhost/dvwa/vulnerabilities/csp/#', 'method': 'post', 'inputs': [{'name': None, 'type': 'button', 'value': 'Solve the sum'}]}
{'page': 'http://localhost/dvwa/vulnerabilities/csp/', 'action': 'http://localhost/dvwa/vulnerabilities/csp/', 'method': 'post', 'inputs': [{'name': None, 'type': 'button', 'value': 'Solve the sum'}]}
{'page': 'http://localhost/dvwa/vulnerabilities/xss_s/#', 'action': 'http://localhost/dvwa/vulnerabilities/xss_s/#', 'method': 'post', 'inputs': [{'name': 'txtName', 'type': 'text', 'value': ''}, {'name': 'btnSign', 'type': 'submit', 'value': 'Sign Guestbook'}, {'name': 'btnClear', 'type': 'submit', 'value': 'Clear Guestbook'}, {'name': 'user_token', 'type': 'hidden', 'value': '762495a75dc9c1600bb79c49335ee13d'}]}
{'page': 'http://localhost/dvwa/vulnerabilities/xss_s/', 'action': 'http://localhost/dvwa/vulnerabilities/xss_s/', 'method': 'post', 'inputs': [{'name': 'txtName', 'type': 'text', 'value': ''}, {'name': 'btnSign', 'type': 'submit', 'value': 'Sign Guestbook'}, {'name': 'btnClear', 'type': 'submit', 'value': 'Clear Guestbook'}, {'name': 'user_token', 'type': 'hidden', 'value': '75c7d5777269ba2bff5a50968f53db78'}]}
{'page': 'http://localhost/dvwa/vulnerabilities/xss_r/#', 'action': 'http://localhost/dvwa/vulnerabilities/xss_r/#', 'method': 'get', 'inputs': [{'name': 'name', 'type': 'text', 'value': ''}, {'name': None, 'type': 'submit', 'value': 'Submit'}, {'name': 'user_token', 'type': 'hidden', 'value': '9f1587e39ce7cfc66aa2dcce14186a27'}]}
{'page': 'http://localhost/dvwa/vulnerabilities/xss_r/', 'action': 'http://localhost/dvwa/vulnerabilities/xss_r/#', 'method': 'get', 'inputs': [{'name': 'name', 'type': 'text', 'value': ''}, {'name': None, 'type': 'submit', 'value': 'Submit'}, {'name': 'user_token', 'type': 'hidden', 'value': 'bbf6b01a406c607f98fe098afd186d33'}]}
{'page': 'http://localhost/dvwa/vulnerabilities/xss_d/#', 'action': 'http://localhost/dvwa/vulnerabilities/xss_d/#', 'method': 'get', 'inputs': [{'name': None, 'type': 'submit', 'value': 'Select'}]}
{'page': 'http://localhost/dvwa/vulnerabilities/xss_d/', 'action': 'http://localhost/dvwa/vulnerabilities/xss_d/', 'method': 'get', 'inputs': [{'name': None, 'type': 'submit', 'value': 'Select'}]}
{'page': 'http://localhost/dvwa/vulnerabilities/weak_id/#', 'action': 'http://localhost/dvwa/vulnerabilities/weak_id/#', 'method': 'post', 'inputs': [{'name': None, 'type': 'submit', 'value': 'Generate'}]}
{'page': 'http://localhost/dvwa/vulnerabilities/weak_id/', 'action': 'http://localhost/dvwa/vulnerabilities/weak_id/', 'method': 'post', 'inputs': [{'name': None, 'type': 'submit', 'value': 'Generate'}]}
{'page': 'http://localhost/dvwa/vulnerabilities/sqli_blind/#', 'action': 'http://localhost/dvwa/vulnerabilities/sqli_blind/#', 'method': 'get', 'inputs': [{'name': 'id', 'type': 'text', 'value': ''}, {'name': 'Submit', 'type': 'submit', 'value': 'Submit'}, {'name': 'user_token', 'type': 'hidden', 'value': '7a1578585ae31ac8527ffb75e56229aa'}]}
{'page': 'http://localhost/dvwa/vulnerabilities/sqli_blind/', 'action': 'http://localhost/dvwa/vulnerabilities/sqli_blind/#', 'method': 'get', 'inputs': [{'name': 'id', 'type': 'text', 'value': ''}, {'name': 'Submit', 'type': 'submit', 'value': 'Submit'}, {'name': 'user_token', 'type': 'hidden', 'value': 'af2e3be5613cb9da8099bc6d8a6300d1'}]}
{'page': 'http://localhost/dvwa/vulnerabilities/sqli/#', 'action': 'http://localhost/dvwa/vulnerabilities/sqli/#', 'method': 'get', 'inputs': [{'name': 'id', 'type': 'text', 'value': ''}, {'name': 'Submit', 'type': 'submit', 'value': 'Submit'}, {'name': 'user_token', 'type': 'hidden', 'value': '2d44fb575e822bca342856eac70a2aa7'}]}
{'page': 'http://localhost/dvwa/vulnerabilities/sqli/', 'action': 'http://localhost/dvwa/vulnerabilities/sqli/#', 'method': 'get', 'inputs': [{'name': 'id', 'type': 'text', 'value': ''}, {'name': 'Submit', 'type': 'submit', 'value': 'Submit'}, {'name': 'user_token', 'type': 'hidden', 'value': '85ad35562b7d5dc6354edfc1fc4a8c01'}]}
{'page': 'http://localhost/dvwa/vulnerabilities/captcha/#', 'action': 'http://localhost/dvwa/vulnerabilities/captcha/#', 'method': 'post', 'inputs': [{'name': 'step', 'type': 'hidden', 'value': '1'}, {'name': 'password_current', 'type': 'password', 'value': ''}, {'name': 'password_new', 'type': 'password', 'value': ''}, {'name': 'password_conf', 'type': 'password', 'value': ''}, {'name': 'user_token', 'type': 'hidden', 'value': '549089a616c058507e27080a5aeaa76d'}, {'name': 'Change', 'type': 'submit', 'value': 'Change'}]}
{'page': 'http://localhost/dvwa/vulnerabilities/captcha/', 'action': 'http://localhost/dvwa/vulnerabilities/captcha/#', 'method': 'post', 'inputs': [{'name': 'step', 'type': 'hidden', 'value': '1'}, {'name': 'password_current', 'type': 'password', 'value': ''}, {'name': 'password_new', 'type': 'password', 'value': ''}, {'name': 'password_conf', 'type': 'password', 'value': ''}, {'name': 'user_token', 'type': 'hidden', 'value': '867c80211bbf5b6e36bbb1346a8ef32a'}, {'name': 'Change', 'type': 'submit', 'value': 'Change'}]}
{'page': 'http://localhost/dvwa/vulnerabilities/upload/#', 'action': 'http://localhost/dvwa/vulnerabilities/upload/#', 'method': 'post', 'inputs': [{'name': 'MAX_FILE_SIZE', 'type': 'hidden', 'value': '100000'}, {'name': 'uploaded', 'type': 'file', 'value': ''}, {'name': 'Upload', 'type': 'submit', 'value': 'Upload'}, {'name': 'user_token', 'type': 'hidden', 'value': 'e455c4eda27120c95b94f2801ddb621d'}]}
{'page': 'http://localhost/dvwa/vulnerabilities/upload/', 'action': 'http://localhost/dvwa/vulnerabilities/upload/#', 'method': 'post', 'inputs': [{'name': 'MAX_FILE_SIZE', 'type': 'hidden', 'value': '100000'}, {'name': 'uploaded', 'type': 'file', 'value': ''}, {'name': 'Upload', 'type': 'submit', 'value': 'Upload'}, {'name': 'user_token', 'type': 'hidden', 'value': '0c667a98e1e65cbb1fea4ec6c60bfa59'}]}
{'page': 'http://localhost/dvwa/vulnerabilities/fi/?page=file1.php', 'action': 'http://localhost/dvwa/vulnerabilities/fi/login.php', 'method': 'post', 'inputs': [{'name': 'username', 'type': 'text', 'value': ''}, {'name': 'password', 'type': 'password', 'value': ''}, {'name': 'Login', 'type': 'submit', 'value': 'Login'}, {'name': 'user_token', 'type': 'hidden', 'value': '437efbcd7d74fef6f581886584f534d4'}]}
{'page': 'http://localhost/dvwa/vulnerabilities/fi/?page=file2.php', 'action': 'http://localhost/dvwa/vulnerabilities/fi/login.php', 'method': 'post', 'inputs': [{'name': 'username', 'type': 'text', 'value': ''}, {'name': 'password', 'type': 'password', 'value': ''}, {'name': 'Login', 'type': 'submit', 'value': 'Login'}, {'name': 'user_token', 'type': 'hidden', 'value': '8c0e8e1f09d3d733576f9e1228257dd0'}]}
{'page': 'http://localhost/dvwa/vulnerabilities/fi/?page=file3.php', 'action': 'http://localhost/dvwa/vulnerabilities/fi/login.php', 'method': 'post', 'inputs': [{'name': 'username', 'type': 'text', 'value': ''}, {'name': 'password', 'type': 'password', 'value': ''}, {'name': 'Login', 'type': 'submit', 'value': 'Login'}, {'name': 'user_token', 'type': 'hidden', 'value': '46b69cb66dc5a4c47224695d7716dcd5'}]}
{'page': 'http://localhost/dvwa/vulnerabilities/csrf/#', 'action': 'http://localhost/dvwa/vulnerabilities/csrf/#', 'method': 'get', 'inputs': [{'name': 'password_current', 'type': 'password', 'value': ''}, {'name': 'password_new', 'type': 'password', 'value': ''}, {'name': 'password_conf', 'type': 'password', 'value': ''}, {'name': 'Change', 'type': 'submit', 'value': 'Change'}, {'name': 'user_token', 'type': 'hidden', 'value': '05c11f434a46541aa7e1600d7dff12c8'}]}
{'page': 'http://localhost/dvwa/vulnerabilities/csrf/', 'action': 'http://localhost/dvwa/vulnerabilities/csrf/#', 'method': 'get', 'inputs': [{'name': 'password_current', 'type': 'password', 'value': ''}, {'name': 'password_new', 'type': 'password', 'value': ''}, {'name': 'password_conf', 'type': 'password', 'value': ''}, {'name': 'Change', 'type': 'submit', 'value': 'Change'}, {'name': 'user_token', 'type': 'hidden', 'value': '4733db826fbff1584e8e69cf83409d36'}]}
{'page': 'http://localhost/dvwa/vulnerabilities/exec/#', 'action': 'http://localhost/dvwa/vulnerabilities/exec/#', 'method': 'post', 'inputs': [{'name': 'ip', 'type': 'text', 'value': ''}, {'name': 'Submit', 'type': 'submit', 'value': 'Submit'}, {'name': 'user_token', 'type': 'hidden', 'value': 'b0e73cf92c84bf93b61499d034b28948'}]}
{'page': 'http://localhost/dvwa/vulnerabilities/exec/', 'action': 'http://localhost/dvwa/vulnerabilities/exec/#', 'method': 'post', 'inputs': [{'name': 'ip', 'type': 'text', 'value': ''}, {'name': 'Submit', 'type': 'submit', 'value': 'Submit'}, {'name': 'user_token', 'type': 'hidden', 'value': '59ff771b0ec79b837841daa3e72e3b9b'}]}
{'page': 'http://localhost/dvwa/vulnerabilities/brute/#', 'action': 'http://localhost/dvwa/vulnerabilities/brute/#', 'method': 'post', 'inputs': [{'name': 'username', 'type': 'text', 'value': ''}, {'name': 'password', 'type': 'password', 'value': ''}, {'name': 'Login', 'type': 'submit', 'value': 'Login'}, {'name': 'user_token', 'type': 'hidden', 'value': '1428c9a05c126a6c62bf3fa7195a6d9b'}]}
{'page': 'http://localhost/dvwa/vulnerabilities/brute/', 'action': 'http://localhost/dvwa/vulnerabilities/brute/#', 'method': 'post', 'inputs': [{'name': 'username', 'type': 'text', 'value': ''}, {'name': 'password', 'type': 'password', 'value': ''}, {'name': 'Login', 'type': 'submit', 'value': 'Login'}, {'name': 'user_token', 'type': 'hidden', 'value': '9210ed454fdd53aaecdb23df58a972a1'}]}
{'page': 'http://localhost/dvwa/setup.php#', 'action': 'http://localhost/dvwa/setup.php#', 'method': 'post', 'inputs': [{'name': 'create_db', 'type': 'submit', 'value': 'Create / Reset Database'}, {'name': 'user_token', 'type': 'hidden', 'value': 'd4102b4cf1b3257732ddd5ef70aa84bd'}]}
{'page': 'http://localhost/dvwa/setup.php', 'action': 'http://localhost/dvwa/setup.php#', 'method': 'post', 'inputs': [{'name': 'create_db', 'type': 'submit', 'value': 'Create / Reset Database'}, {'name': 'user_token', 'type': 'hidden', 'value': 'a99a5b715e19d2ca0eaeb2562374c210'}]}

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

### 🐍 Python Version Verification  

![Python Version](Week-2/screenshots/py_version.png)

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
