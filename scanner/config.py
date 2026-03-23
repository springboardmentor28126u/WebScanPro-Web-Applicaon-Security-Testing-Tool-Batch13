TARGET_URL = "http://localhost"
LOGIN_URL  = "http://localhost/login.php"
USERNAME      = "admin"
PASSWORD      = "password"
DVWA_SECURITY = "low"

# Session cookie — copy from browser DevTools after login
COOKIES = {
    "PHPSESSID": "j7ksf6cb27pekelcm0k933jq26",
    "security": "low"
}

# Payload file paths (relative to project root)
SQL_PAYLOADS_FILE = "payloads/sql_payloads.txt"
XSS_PAYLOADS_FILE = "payloads/xss_payloads.txt"

# Report output paths
REPORT_OUTPUT = "reports/security_report.html"
RESULTS_JSON  = "reports/results.json"

