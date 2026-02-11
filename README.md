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

This makes vulnerabilities easier to understand for beginners.

---

### Step 3: Explore Vulnerability Modules

DVWA includes modules such as:

* SQL Injection
* Cross-Site Scripting (XSS)
* Command Injection
* File Upload
* Brute Force Attacks

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
