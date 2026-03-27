import requests
import time

API_KEY = "MY_API_KEY"

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def fallback_analysis(vuln_type):
    """Return fallback text if Gemini fails"""
    fallback = {
        "SQL Injection": (
            "1. The application inserts user input directly into SQL queries "
            "without sanitization, allowing attackers to manipulate the database.\n"
            "2. An attacker can extract all usernames and passwords, bypass login, "
            "or delete entire database tables.\n"
            "3. Use parameterized queries or prepared statements. Never concatenate "
            "user input into SQL strings directly."
        ),
        "Cross Site Scripting": (
            "1. User input is reflected directly in the web page without encoding, "
            "allowing JavaScript code to execute in the victim's browser.\n"
            "2. An attacker can steal session cookies, hijack user accounts, "
            "redirect users to malicious sites, or deface the page.\n"
            "3. Encode all output using HTML entity encoding and implement "
            "Content Security Policy headers."
        ),
        "Brute Force": (
            "1. The login page has no protection against repeated login attempts, "
            "allowing automated tools to try thousands of passwords.\n"
            "2. An attacker can systematically guess credentials until they find "
            "a valid username and password, gaining full account access.\n"
            "3. Implement account lockout after 3 to 5 failed attempts, add CAPTCHA, "
            "enforce strong password policy, and enable Multi-Factor Authentication."
        ),
        "IDOR": (
            "1. The application uses direct object references in URLs without "
            "checking if the logged-in user owns the requested resource.\n"
            "2. An attacker can access, modify, or delete any other user's data "
            "simply by changing the ID parameter in the URL.\n"
            "3. Implement Role-Based Access Control and validate object ownership "
            "on every request server-side before returning data."
        ),
        "Session Management": (
            "1. Session cookies are missing security flags like HttpOnly and Secure, "
            "making them vulnerable to theft and interception.\n"
            "2. An attacker can steal session cookies using XSS attacks or network "
            "sniffing, then use them to impersonate logged-in users.\n"
            "3. Set HttpOnly, Secure and SameSite flags on all cookies. Regenerate "
            "session tokens on login and invalidate them on logout."
        ),
        "Vertical Privilege Escalation": (
            "1. The application does not properly restrict access to admin pages, "
            "allowing low-privilege users to access sensitive functionality.\n"
            "2. An attacker with a normal user account can access admin panels, "
            "change security settings, or view all user data.\n"
            "3. Enforce server-side role checks on every protected page. Never "
            "rely on hiding links — always verify user role before serving content."
        ),
    }
    return fallback.get(
        vuln_type,
        "1. Security misconfiguration detected in this module.\n"
        "2. This may allow unauthorized access to sensitive data or functionality.\n"
        "3. Apply proper input validation, authentication and access control."
    )


def ask_gemini(prompt, vuln_type="General", max_tokens=150):
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "openai/gpt-4o-mini",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": max_tokens
        }

        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=30
        )

        print("\n------ AI RESPONSE ------")
        print(response.text)
        print("-------------------------")

        if response.status_code != 200:
            return fallback_analysis(vuln_type)

        data = response.json()

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        print("AI error:", e)
        return fallback_analysis(vuln_type)
def analyze_vulnerability(vuln_type, payload, status, severity, endpoint, max_tokens=120):
    """Get AI mitigation only for vulnerability."""
    
    prompt = (
        f"You are a cybersecurity expert.\n\n"
        f"Vulnerability Type: {vuln_type}\n"
        f"Endpoint: {endpoint}\n"
        f"Severity: {severity}\n\n"
        f"Give ONLY mitigation steps.\n"
        f"Do not explain the vulnerability.\n"
        f"Do not give attacker impact.\n\n"
        f"Return exactly:\n"
        f"- 3 bullet point mitigation steps\n"
        f"- short and direct\n"
        f"- for developer\n"
    )

    return ask_gemini(prompt, vuln_type, max_tokens)


def analyze_full_report(sqli_results, xss_results, brute_force_results, privilege_results):
    """Get AI overall risk assessment for the full scan."""

    vuln_sqli  = sum(1 for _, s, _ in sqli_results if s == "Vulnerable")
    vuln_xss   = sum(1 for _, s, _ in xss_results if s == "Reflected")
    vuln_idor  = sum(1 for _, s, _ in privilege_results if s == "Accessible")
    vuln_brute = 1 if brute_force_results else 0

    prompt = (
        f"You are a cybersecurity expert reviewing a full security scan report.\n\n"
        f"Scan Results:\n"
        f"- SQL Injection : {vuln_sqli} out of {len(sqli_results)} payloads Vulnerable\n"
        f"- XSS           : {vuln_xss} out of {len(xss_results)} payloads Reflected\n"
        f"- Brute Force   : {'Weak credential admin:password found' if vuln_brute else 'None found'}\n"
        f"- IDOR          : {vuln_idor} out of {len(privilege_results)} IDs Accessible\n\n"
        f"Give me all of these on separate numbered lines:\n"
        f"1. Overall Risk Level — Critical / High / Medium / Low\n"
        f"2. Risk Score out of 10 with brief reason\n"
        f"3. Top 3 most dangerous findings with one line explanation each\n"
        f"4. Top 3 recommended fixes with specific steps\n"
        f"5. One sentence overall summary\n\n"
        f"Explain this vulnerability in 3–4 lines for a report."
    )
    return ask_gemini(prompt, "Full Report")
