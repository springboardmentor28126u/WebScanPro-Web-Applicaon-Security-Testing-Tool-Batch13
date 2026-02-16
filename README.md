## **WebScanPro Automated Web Application Security Testing Tool**



###### WebScanPro is a modular web application vulnerability scanner developed

###### as part of an internship project to gain practical insight into how

###### automated security testing tools function internally.



###### The system is designed to scan a target web application, locate possible

###### input points, send controlled test payloads, analyze server responses,

###### and produce structured reports highlighting potential security

###### weaknesses.

###### 

###### For development and testing purposes, DVWA (Damn Vulnerable Web

###### Application) was used as a controlled environment to safely study and

###### validate vulnerability detection techniques.



#### **Milestone 1 – Project Initialization \& Target Scanning**



###### The first milestone concentrated on setting up the testing environment

###### and building the initial crawling mechanism necessary for automated

###### vulnerability assessment.



#### **Week 1 – Project Initialization \& Environment Setup**



###### **Project Objectives**

###### 

###### The main aim of WebScanPro is to create a scalable and modular web

###### vulnerability scanner capable of detecting common security flaws aligned

###### with the OWASP Top 10 vulnerability categories.

###### 

###### **Key Learning Goals**

###### 

###### \-   Understanding fundamental web security concepts

###### \-   Studying HTTP request–response communication

###### \-   Identifying vulnerability patterns in web forms and URLs

###### \-   Performing manual vulnerability testing before automation

###### \-   Designing a structured workflow for automated scanning

###### 

###### **Development Environment Setup**

###### 

###### A controlled testing environment was prepared using the following tools

###### and technologies:

###### 

###### **Tools \& Technologies Used**

###### 

###### \-   Python – Primary programming language for development

###### \-   Virtual Environment (venv) – Dependency and package isolation

###### \-   Requests Library – Handling HTTP communication

###### \-   BeautifulSoup – Parsing and analyzing HTML content

###### \-   Selenium – Planned for future browser automation tasks

###### \-   XAMPP Server – Local Apache, PHP, and MySQL environment for hosting

###### &nbsp;   DVWA

###### 

###### **DVWA Deployment Using XAMPP**

###### 

###### DVWA was hosted locally using XAMPP, which provides an integrated Apache

###### server, PHP interpreter, and MySQL database.

###### 

###### **Using XAMPP offered several advantages:**

###### 

###### \-   Simple local server setup

###### \-   Full control over web server configuration

###### \-   Safe environment for vulnerability experimentation

###### \-   Easy management of database and web application components

###### 

###### This setup allowed realistic testing without exposing any systems to

###### external risk.

###### 

###### **Manual Exploration \& Vulnerability Analysis**

###### 

###### Before automation, DVWA was manually explored to understand:

###### 

###### \-   Application navigation structure

###### \-   Login and authentication flow

###### \-   Input forms and parameter handling

###### \-   Built-in vulnerable modules

###### 

###### **Manual Vulnerability Testing Included**

###### 

###### \-   SQL Injection

###### \-   Reflected Cross-Site Scripting (XSS)

###### \-   Stored XSS

###### \-   Command Injection

###### 

###### This phase helped build a practical understanding of how vulnerabilities

###### manifest before developing automated detection mechanisms.



#### **Week 2 – Target Scanning Module Development**



###### During the second week, the focus shifted toward automating attack

###### surface discovery through the implementation of a crawler module.



###### **Crawler Module Development (crawler.py)**



###### The crawler was designed to automatically:

###### 

###### \-   Discover internal web pages

###### \-   Extract hyperlinks within the application

###### \-   Identify HTML forms

###### \-   Detect input fields

###### \-   Capture GET and POST request parameters

###### 

###### This automated process helps identify potential injection points

###### efficiently.

###### 

###### **HTML Parsing with BeautifulSoup**

###### 

###### BeautifulSoup was used to:

###### 

###### \-   Parse HTML responses from target pages

###### \-   Identify links for further crawling

###### \-   Extract form elements and input fields

###### \-   Collect attributes required for testing

###### 

###### This enables systematic identification of interactive components within

###### web applications.

###### 

###### **Structured Metadata for Testing Modules**

###### 

###### Extracted data was organized into structured metadata, including:

###### 

###### \-   Form action URLs

###### \-   Input field names

###### \-   HTTP request methods (GET/POST)

###### \-   Discovered application endpoints

###### 

###### This structured information feeds subsequent vulnerability testing

###### modules such as:

###### 

###### \-   SQL Injection Scanner

###### \-   Cross-Site Scripting (XSS) Scanner

###### 

###### Workflow Achieved by the End of Week 2

###### 

###### By the completion of Week 2, the system was able to:

###### 

###### \-   Establish a connection with the target web application

###### \-   Automatically crawl application pages

###### \-   Extract forms and parameters

###### \-   Prepare structured input data for vulnerability testing modules

###### 

###### This formed the technical base required for implementing automated

###### vulnerability detection in later stages.

###### 

###### **Milestone 1 Outcome**

###### 

###### \-   Fully configured local testing environment using XAMPP

###### \-   Successful DVWA deployment for safe vulnerability testing

###### \-   Manual validation of common vulnerabilities

###### \-   Implementation of an automated crawling module

###### \-   Structured mapping of application attack surfaces

