# 🚀 WebScanPro  
### Automated Web Application Security Testing Tool  

WebScanPro is a modular automated web vulnerability scanner developed as part of an internship project to understand how security testing tools operate internally.  

The tool is designed to scan a target web application, identify input surfaces, inject test payloads, analyze server responses, and generate structured vulnerability findings.  

DVWA (Damn Vulnerable Web Application) is used as the controlled testing environment for development and validation.

---

# 📌 Milestone 1 – Project Initialization & Target Scanning

Milestone 1 focused on establishing the testing environment and developing the foundational crawling module required for automated vulnerability detection.

---

# 📅 Week 1 – Project Initialization & Environment Setup

## 🎯 Project Goals and Objectives

The objective of WebScanPro is to design a scalable and modular vulnerability scanning tool capable of detecting common web application vulnerabilities aligned with OWASP Top 10 standards.

### Key Goals

- Understand web application security fundamentals  
- Study HTTP request–response lifecycle  
- Explore vulnerability patterns in web forms and URLs  
- Perform manual testing before automation  
- Design structured scanning workflow  

---

## 🛠 Development Environment Setup

To build a secure and controlled lab environment, the following tools were installed:

### Tools & Technologies

- **Python** – Core programming language  
- **Virtual Environment (venv)** – Dependency isolation  
- **Requests Library** – HTTP communication  
- **BeautifulSoup** – HTML parsing  
- **Selenium** – Future browser automation  
- **Docker Desktop** – Containerized deployment  

---

## 🐳 DVWA Deployment Using Docker

DVWA was deployed using Docker to simulate a vulnerable web application.

### Pull DVWA Image 


```bash
docker pull vulnerables/web-dvwa
### Purpose of Docker```

- Provides isolated environment
- No manual configuration of Apache/PHP/MySQL
- Easy start and stop management
- Safe vulnerability testing setup

## 🔎 Manual Exploration & Vulnerability Understanding

DVWA was manually explored to understand:

- Website navigation flow
- Authentication mechanisms
- Forms and input parameters
- Built-in vulnerable modules

 ### Manual Testing Conducted:
- SQL Injection
- Reflected XSS
- Stored XSS
- Command Injection

This helped in understanding how vulnerabilities behave before automating detection logic.

# 📅 Week 2 – Target Scanning Module Development

Week 2 focused on automating the discovery of attack surfaces through implementation of the crawler module.

## 🕷 Crawler Module Design (crawler.py)

The crawler module was implemented to automatically:

- Discover internal web pages
- Extract hyperlinks
- Identify HTML forms
- Detect input fields
- Capture GET and POST parameters

This automated the process of identifying injection points.

## 🧩 HTML Parsing Using BeautifulSoup

The crawler uses BeautifulSoup to:

- Parse HTML response content
- Extract <a> tags for link discovery
- Extract <form> elements
- Collect <input> field attributes

This allows the scanner to programmatically locate interactive components.

## 📊 Metadata Structuring for Testing Modules

The extracted data is structured into organized metadata including:

- Form action URLs
- Input field names
- HTTP request methods (GET/POST)
- Discovered endpoints

This structured information is then passed to vulnerability testing modules such as:

~ SQL Injection Scanner

~ XSS Scanner

## 🔁 Workflow Established by End of Week 2

By the end of Week 2, the system could:

- Connect to the target application
- Crawl pages automatically
- Extract forms and parameters
- Prepare structured input data for testing modules

This created the technical foundation required for implementing automated vulnerability detection in the next milestone.

# ✅ Milestone 1 Outcome

- Fully configured testing lab environment
- Successful deployment of DVWA
- Manual validation of vulnerabilities
- Implementation of automated crawler
- Structured attack surface mapping

Milestone 1 successfully established the core infrastructure and discovery engine required for WebScanPro.
    
