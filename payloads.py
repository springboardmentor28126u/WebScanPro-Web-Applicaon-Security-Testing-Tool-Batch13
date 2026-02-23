# payloads.py
SQLI_PAYLOADS = ["'", "''", "';--", "' OR '1'='1", "' OR 1=1 --"]
XSS_PAYLOADS = ["<script>alert('XSS')</script>", "<u>Test</u>", "<img src=x onerror=alert(1)>"]

# Keywords that indicate a database error happened
SQL_ERRORS = [
    "you have an error in your sql syntax",
    "warning: mysql",
    "unclosed quotation mark",
    "quoted string not properly terminated"
]