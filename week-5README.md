# Week 5 – Authentication and Brute Force Testing

## Objective

The goal of this week is to test authentication mechanisms of the web application and identify weaknesses such as weak passwords or lack of login protection.

## Environment

* XAMPP Local Server
* DVWA (Damn Vulnerable Web Application)
* Python
* Requests Library

## Tasks Performed

* Analyzed the login functionality of the web application.
* Created a Python script to perform brute force testing on the login page.
* Used a list of common usernames and passwords to attempt login.
* Checked if the application allows unlimited login attempts.

## Tools and Technologies

* Python
* Requests Library
* DVWA Web Application

## Outcome

The brute force testing script was able to identify possible valid login credentials by trying multiple username and password combinations. This demonstrates the risk of weak authentication mechanisms.

## Security Recommendations

* Implement account lockout after multiple failed login attempts.
* Use strong password policies.
* Add CAPTCHA or multi-factor authentication to prevent automated attacks.

## Conclusion

This week's work helped in understanding authentication vulnerabilities and how brute force attacks can compromise user accounts if proper security controls are not implemented.
