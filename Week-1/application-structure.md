# DVWA Application Structure Exploration

## Objective
To explore the structure and functionality of DVWA and understand how different modules represent real-world web vulnerabilities.

## Application Overview
DVWA is an intentionally vulnerable PHP/MySQL web application designed to help understand common web security issues in a legal environment.

## Key Sections
- Home: Overview and usage instructions.
- DVWA Security: Allows changing security levels (Low, Medium, High).
- Setup / Reset DB: Used to initialize or reset the database.

## Vulnerability Modules Explored
- Brute Force: Demonstrates weak authentication mechanisms.
- SQL Injection: Shows how improper input handling leads to database attacks.
- XSS (Reflected, Stored, DOM): Demonstrates client-side script injection.
- Command Injection: Shows execution of system commands via user input.
- File Upload: Demonstrates insecure file handling.

## Security Levels
- Low: Minimal protection, easy to exploit.
- Medium/High: Incremental security controls.
- Impossible: Secure implementation.

## Relevance to WebScanPro
The DVWA modules directly map to the planned WebScanPro scanning modules such as SQL Injection testing, XSS testing, and authentication testing.

## Outcome
The exploration provided a clear understanding of DVWA’s internal structure and vulnerability flow, which will be used as a baseline for designing automated scanning logic in later stages.
