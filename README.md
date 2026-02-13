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
