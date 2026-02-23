class SQLScanner:

    def __init__(self, session):
        self.session = session

    def test_get_parameter(self, url, param_name):

        vulnerabilities = []

        true_payload = "' OR '1'='1"
        false_payload = "' AND '1'='2"

        true_url = f"{url}?{param_name}={true_payload}&Submit=Submit"
        false_url = f"{url}?{param_name}={false_payload}&Submit=Submit"

        true_response = self.session.get(true_url)
        false_response = self.session.get(false_url)

        # 🔴 Session check
        if "Login :: Damn Vulnerable" in true_response.text:
            print("Session expired")
            return []

        # 🔥 1️⃣ ERROR-BASED DETECTION (ADD HERE)
        error_patterns = [
            "SQL syntax",
            "mysql_fetch",
            "Warning: mysql",
            "You have an error in your SQL syntax"
        ]

        for pattern in error_patterns:
            if pattern in true_response.text:
                vulnerabilities.append({
                    "url": true_url,
                    "parameter": param_name,
                    "type": "SQL Injection (Error-Based)",
                    "severity": "High",
                    "fix": "Sanitize input and use prepared statements."
                })
                return vulnerabilities

        # 🔥 2️⃣ BOOLEAN-BASED DETECTION
        baseline = self.session.get(url, params={param_name: "1"})

        baseline_text = baseline.text
        true_text = true_response.text
        false_text = false_response.text

        if (
            true_text != false_text
            and true_text != baseline_text
            and false_text == baseline_text
        ):
            vulnerabilities.append({
                "url": true_url,
                "parameter": param_name,
                "type": "SQL Injection (Boolean-Based)",
                "severity": "High",
                "fix": "Use parameterized queries."
            })

        return vulnerabilities