WEBSCANPRO - Web Application Security Testing Tool

Week 1 – Project Setup

WebScanPro is a tool that checks websites for common security problems like:

  1.SQL Injection

  2.Cross-Site Scripting (XSS)

  3.Weak login systems




Tools Used:

   1.XAMPP (Apache & MySQL server)
 
   2.DVWA (Vulnerable test website)

   3.Python

   4.Git & GitHub

   5.Web Browser



Environment setup:

   1.Installed XAMPP

   2.Started Apache & MySQL

   3.Installed DVWA inside htdocs

   4.Created dvwa database

   5.Configured and ran DVWA

   6.Logged into DVWA successfully

<img width="825" height="419" alt="image" src="https://github.com/user-attachments/assets/03673582-8317-4f4b-a32f-243ae2aed60f" />

<img width="809" height="472" alt="image" src="https://github.com/user-attachments/assets/d16824ac-063e-4e69-8f62-b3bd68ac148c" />

<img width="825" height="440" alt="image" src="https://github.com/user-attachments/assets/095c9a62-f5bf-42d4-8b32-04d4270e90ae" />

<img width="825" height="482" alt="image" src="https://github.com/user-attachments/assets/a233d6ae-0dd0-463a-979e-40abcface13c" />

<img width="825" height="435" alt="image" src="https://github.com/user-attachments/assets/5d53c0b5-f90f-47bf-a707-3432d7964240" />

<img width="825" height="503" alt="image" src="https://github.com/user-attachments/assets/03824920-4602-4015-b6e9-c3ec168a75aa" />


Result:

DVWA running successfully

Vulnerability pages identified

Ready for automation



Week 2 – Target Scanning Module

Create a Python scanner to automatically find:

1.Forms

2.Input fields

3.Form action URLs

4.GET/POST methods

This helps in future automated testing.

Scanner.py:

--Starts from http://localhost/dvwa/

--Sends request to the page

--Reads HTML content

--Finds <form> tags

Extracts:

--Form action

--Method

--Input names

--Input types

Saves results into:

--output.json

--output.txt

output:

Page URL

Form action

Method

Input fields





