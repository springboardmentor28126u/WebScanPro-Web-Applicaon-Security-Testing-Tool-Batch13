# WebScanPro-Web-Applicaon-Security-Testing-Tool-Batch13
## Milestone 1 Progress Report

**Status:** Completed ✅

---

## 📋 Overview
I have successfully completed the foundation of **WebScanPro**. This milestone focused on establishing a secure testing environment and developing the initial automated discovery module.

## 🛠️ Phase 1: Environment Setup (Week 1)
I have deployed intentionally vulnerable applications to serve as targets for our scanner. These are hosted locally to ensure a safe and legal testing environment.

| Target Application | Deployment Method | URL |
| :--- | :--- | :--- |
| **DVWA** | Docker / PHP Stack | `http://localhost:8080` |
| **OWASP Juice Shop** | Docker / Node.js SPA | `http://localhost:3000` |

#### **Week 1 Evidence:**
![DVWA Setup Screenshot](./dvwa_setup.jpeg)
*Figure 1: The DVWA login and home interface running locally.*

> **Student Note:** I verified that DVWA is running correctly. I noticed its structure is highly dependent on session cookies, which I will need to handle in the next phase.

---

## 🔍 Phase 2: Target Scanning Module (Week 2)
I developed `scanner.py`, a Python-based discovery engine that identifies "Entry Points" for potential attacks.

### Technical Implementation:
* **Library:** Used `BeautifulSoup` for HTML parsing and `Requests` for HTTP communication.
* **Logic:** The script mimics a real browser using a `User-Agent` header to fetch the page and extract interactive elements.
* **Findings:**
    * Successfully identified **Email** and **Password** fields on the login page.
    * Detected the **Login Button** as the submission trigger.
    * Confirmed that **Juice Shop** is an SPA (Single Page Application), which will require dynamic scanning later.
#### **Week 2 Evidence:**
![Scanner Execution Screenshot](./scanner_result.jpeg)
*Figure 2: Terminal output showing the scanner successfully identifying email and password fields.*
### Sample Output:
```text
[+] DISCOVERED INPUT FIELDS:
 -> [FOUND] Email Field (id: email)
 -> [FOUND] Password Field (id: password)
 -> [FOUND] Login Button
