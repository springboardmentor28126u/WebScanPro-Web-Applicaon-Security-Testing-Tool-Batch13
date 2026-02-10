# DVWA Setup on XAMPP

## Objective
To set up Damn Vulnerable Web Application (DVWA) on a local environment using XAMPP for security testing and learning purposes.

## Environment Details
- Operating System: Windows
- Web Server: Apache (XAMPP)
- Database: MySQL
- Application: DVWA
- PHP Version: 8.x

## Setup Steps
1. Installed XAMPP and started Apache and MySQL services.
2. Downloaded DVWA and placed it inside the `htdocs` directory.
3. Created a MySQL database named `dvwa` using phpMyAdmin.
4. Configured `config.inc.php` with correct database credentials.
5. Enabled required PHP settings (`allow_url_fopen`, `allow_url_include`).
6. Initialized the database using the DVWA setup page.
7. Logged into the application using default credentials.

## Verification
- DVWA dashboard loaded successfully.
- All vulnerability modules were visible.
- Application was accessible at `http://localhost/dvwa`.

## Outcome
DVWA was successfully installed and configured on the local server, providing a controlled environment to explore common web application vulnerabilities.
