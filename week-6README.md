# Week 6 – Access Control and IDOR Testing

## Objective

The objective of this week is to test the web application for access control vulnerabilities such as Insecure Direct Object Reference (IDOR) and privilege escalation.

## Environment

* XAMPP Local Server
* DVWA (Damn Vulnerable Web Application)
* Python
* Requests Library

## Tasks Performed

* Analyzed application pages that use parameters such as user IDs.
* Modified ID parameters in the URL to check if unauthorized user data can be accessed.
* Tested horizontal privilege escalation by accessing other users' data.
* Attempted vertical privilege escalation by trying to access restricted pages.
* Created a Python script (`idor_test.py`) to automate testing of multiple ID values.

## Tools and Technologies

* Python
* Requests Library
* DVWA Web Application

## Outcome

By modifying the `id` parameter, different user records were accessed without proper authorization checks. This indicates a potential IDOR vulnerability in the application.

## Security Recommendations

* Implement proper access control checks on the server side.
* Use Role-Based Access Control (RBAC) to restrict access based on user roles.
* Implement Attribute-Based Access Control (ABAC) to ensure users can only access their own data.
* Avoid exposing direct object identifiers in URLs.

## Conclusion

This week's testing helped identify access control weaknesses in the application and demonstrated how improper authorization can lead to unauthorized data access.
