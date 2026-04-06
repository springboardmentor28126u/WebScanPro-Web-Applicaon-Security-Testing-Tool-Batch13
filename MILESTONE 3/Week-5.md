---

## 📄 Week 5: Authentication & Session Testing Module

### 1. What is Authentication & Session Testing?
Authentication testing checks whether a website can be broken into using common or weak passwords. Session testing checks whether the cookie sent after login is properly secured against theft.

**Why it is dangerous:**
- **Weak Passwords:** If a login page has no lockout or rate limiting, an attacker can try thousands of passwords automatically until one works.
- **Cookie Theft:** If session cookies are missing security flags, they can be stolen over plain HTTP or by JavaScript injected via XSS, giving an attacker full account access without needing the password.

---

### 2. How the Module Works (`auth_tester.py`)

**Brute Force (`brute_force`):**
1. Reads passwords one by one from `payloads/passwords.txt`
2. For each password, creates a fresh session and grabs the CSRF token from the login page
3. Sends a POST request with the username, password, and token
4. If the response contains `"Welcome"` or `"logout"` — login succeeded — saves a **HIGH** severity finding and stops

**Cookie Security Check (`check_cookie_security`):**
1. Logs in and inspects the session cookie the server sends back
2. Checks for `Secure` flag — if missing, cookie travels over plain HTTP and can be intercepted
3. Checks for `HttpOnly` flag — if missing, JavaScript can read the cookie and steal it via XSS
4. Missing flags are saved as **MEDIUM** severity findings

---

### 3. Wordlist (`payloads/passwords.txt`)
A list of common weak passwords tried during brute force. The actual DVWA admin password `password` is included so the scanner always finds a result.

