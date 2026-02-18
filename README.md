Tool
📌 Project Overview

WebScanPro is a basic web application security testing tool developed using Python.
The project focuses on scanning web applications, discovering input fields, and preparing data for vulnerability testing.

The tool is tested on intentionally vulnerable platforms such as:

Damn Vulnerable Web Application

📅 Week 1: Project Initialization and Setup
🎯 Project Goals

Understand web application security basics

Set up a local vulnerable testing environment

Explore application structure and vulnerabilities

Prepare environment for automated scanning

⚙ Environment Setup
1️⃣ Install Local Server

Set up a local server using:

XAMPP

Start:

Apache

MySQL

2️⃣ Install Target Application

Download and configure one of the following:

DVWA

Place the application inside the server directory (htdocs if using XAMPP).

3️⃣ Explore Target Application

Analyze:

Website structure

Navigation links

Login forms

Input fields

Common vulnerabilities (SQL Injection, XSS, etc.)

✅ Week 1 Outcome

✔ Local vulnerable application successfully installed
✔ Application running on http://localhost/
✔ Initial understanding of web vulnerabilities

📅 Week 2: Target Scanning Module
🎯 Objective

Develop an automated crawler to scan the target application and extract important testing data.

🛠 Technologies Used

Python

requests library

BeautifulSoup (bs4)

Visual Studio Code

🔍 Crawler Features

The crawler:

Discovers internal web pages

Extracts hyperlinks

Identifies forms

Detects input fields (text, password, textarea, select)

Avoids visiting duplicate pages

📊 Metadata Collection

The crawler collects:

URL list

Form action

Form method (GET/POST)

Input name

Input type

This metadata is stored for future vulnerability testing modules.

▶ How to Run

Ensure Apache and MySQL are running

Open terminal in project folder

Run:

python crawler.py


Output will display discovered pages and form details

✅ Week 2 Outcome

✔ Automated web page discovery
✔ Form and input field extraction
✔ Structured metadata collection
✔ Ready for vulnerability testing module

📁 Project Structure
WebScanPro/
│
├── crawler.py
├── README.md
└── requirements.txt
