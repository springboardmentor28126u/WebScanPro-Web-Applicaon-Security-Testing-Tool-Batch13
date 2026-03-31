# WebScanPro

WebScanPro is a tool I built that automatically tests a website for security vulnerabilities. Instead of manually trying attacks one by one, this tool does it automatically — it logs in, finds all the forms, tries different attacks, checks if they worked, and saves the results.

I tested it on a practice website called DVWA that is made specifically for this kind of security testing.

---

## What Problem Does This Solve?

When a security tester checks a website for vulnerabilities, they have to:
- Find every page and form on the site
- Try different attacks on each one
- Check if the attack worked
- Write down what they found

Doing all of this manually takes a very long time and it's easy to miss things. WebScanPro does all of this automatically.

---

## The Target — DVWA

DVWA stands for Damn Vulnerable Web Application. It is a website that is intentionally built with security holes — it was made so that people can practice finding vulnerabilities in a safe and legal environment.

I ran it on my own computer using Docker:

```bash
docker pull vulnerables/web-dvwa
docker run -d -p 8080:80 vulnerables/web-dvwa
```

After running these commands, DVWA is available at `http://localhost:8080`. I logged in with username `admin` and password `password`, set up the database, and set the security level to Low so that all vulnerabilities are exposed.

---

## Project Folder Structure

```
WebScanPro/
├── crawler/
│   ├── crawler.py           ← finds all pages and forms on the site
│   └── targets.json         ← the list of forms the crawler found
│
├── sql/
│   ├── sqli_tester.py       ← tests for SQL injection
│   └── sqli_findings.json   ← results saved here
│
├── xss/
│   ├── xss.py               ← tests for XSS attacks
│   └── xss_findings.json    ← results saved here
│
├── auth/
│   ├── auth_tester.py       ← tests login and session security
│   └── auth_findings.json   ← results saved here
│
├── idor/
│   ├── idor_tester.py       ← tests access control
│   └── idor_findings.json   ← results saved here
│
├── report/
│   ├── report_generator.py  ← reads all results and makes the HTML report
│   └── report.html          ← the final report you open in a browser
│
└── README.md
```

---

## How Everything Connects

The whole project works like a pipeline where each module feeds into the next:

```
Step 1 — crawler runs → produces targets.json
Step 2 — sqli_tester reads targets.json → produces sqli_findings.json
Step 3 — xss.py reads targets.json → produces xss_findings.json
Step 4 — auth_tester runs → produces auth_findings.json
Step 5 — idor_tester runs → produces idor_findings.json
Step 6 — report_generator reads all findings → produces report.html
```

The crawler only needs to run once. All the testing modules read the same `targets.json` file.

---

## Installation

Install the two Python libraries needed:

```bash
pip install requests beautifulsoup4
```

`requests` is used to send HTTP requests to the website — like a browser but controlled by code.
`beautifulsoup4` is used to read and search through HTML pages.

---

## How to Run

```bash
cd crawler
python crawler.py

cd ../sql
python sqli_tester.py

cd ../xss
python xss.py

cd ../auth
python auth_tester.py

cd ../idor
python idor_tester.py

cd ../report
python report_generator.py
```

After the last step, open `report/report.html` in any browser.

---

## Week 1 — Setting Up the Project

In week 1 I set up DVWA on Docker and manually explored the site. I went through every vulnerability page one by one — SQL injection, XSS, command injection, file upload, brute force, CSRF — and tried attacks manually to understand how each one works.

I also planned out the folder structure and decided how the modules would connect to each other.

---

## Week 2 — Building the Crawler

Before testing anything, I needed to know what pages and forms exist on the site. The crawler does this automatically.

**How the crawler works:**

First it logs in. DVWA's login form has a hidden field called `user_token` — this is a CSRF token that changes every time the page loads. If you don't include it in your login request, the server rejects you. So the crawler:
1. Opens the login page
2. Reads the HTML and finds the `user_token` value using BeautifulSoup
3. Sends the login form with the username, password, and token included

After logging in, it starts at the home page and follows every link it finds. For each page it visits:
- It looks for all `<form>` tags
- For each form it records the action URL (where the form sends data), the method (GET or POST), and all the input field names and types
- It adds the page to a "visited" set so it doesn't visit the same page twice

At the end it saves all of this to `targets.json`.

**Result:** 22 forms found across all DVWA pages including the SQL injection page, XSS pages, brute force page, command injection page, file upload page, and more.

---

## Week 3 — SQL Injection Testing

SQL injection is when you type SQL code into an input field and the website accidentally runs it as a database command. For example, instead of searching for a user, you could make the database dump all its data.

My SQL injection module reads `targets.json` and tests every form that has a text input field.

**How it works:**

Before testing, it sends a normal request with just `id=1` and saves the response. This is called the baseline — I need it to compare against later.

Then it tries 10 different payloads. For each payload it injects it into every text field in the form and sends the request. Then it uses 4 different ways to check if the injection worked:

**Error-Based detection**
I send a single quote `'` which breaks SQL syntax. If the server shows a MySQL error message in the response like `you have an error in your sql syntax`, the input is going straight into the database query without any protection. I detect this using regex pattern matching on the response.

**Boolean-Based detection**
I send `1' OR '1'='1' --` which is always true, and `1' AND 1=2 --` which is always false. A vulnerable site will return different amounts of data for these two. I compare the response size to the baseline — if it changed by more than 30 bytes, the SQL condition affected the result.

**UNION-Based detection**
I send `1' UNION SELECT user(),database() --` which adds an extra SELECT to the query. On a vulnerable site this makes the database return extra data — the current database username and database name. I check if the response grew by more than 50 bytes compared to the baseline. On DVWA it grew by 10,440 bytes which means the whole database info was leaked.

**Time-Based detection**
I send `1' AND SLEEP(3) --` which tells the database to pause for 3 seconds. I measure how long the response takes. If it takes 2.5 seconds or more, blind SQL injection is confirmed. This is useful when the page doesn't show any output — you know the injection worked because the page slows down.

**Results:**
- `/vulnerabilities/sqli/` — vulnerable to Error-Based (High), Boolean-Based (Medium), and UNION-Based (Critical)
- `/vulnerabilities/sqli_blind/` — vulnerable to Time-Based, 3.01 second delay confirmed

All findings saved to `sqli_findings.json`.

---

## Week 4 — XSS Testing

XSS stands for Cross-Site Scripting. It means injecting JavaScript code into a webpage so it runs in someone else's browser. An attacker can use this to steal cookies, hijack sessions, or redirect users to fake sites.

My XSS module reads `targets.json` and filters only the XSS pages.

**How it works:**

I have a list of 11 payloads in 3 categories:
- Basic ones like `<script>alert('XSS')</script>`
- Filter bypass ones like `<ScRiPt>alert('XSS')</ScRiPt>` using mixed case
- DOM-based ones like `#<script>alert('XSS')</script>` that go in the URL hash

For each form I test all 11 payloads. I check for 3 types of XSS:

**Reflected XSS**
I inject the payload into the URL parameter (GET request). If the exact payload appears in the HTML response unchanged, the browser would execute it. I check this with a simple `payload in response_text` check. The page `/xss_r/` had 9 out of 11 payloads trigger.

**Stored XSS**
I inject the payload into the form and submit it (POST request). The payload gets saved in the database. I check if it appears in the page response. This type is more dangerous because every visitor to the page is affected, not just the attacker. Before each test run I send a request to clear the guestbook so old payloads don't cause false results. The page `/xss_s/` had 9 out of 11 trigger.

**DOM-Based XSS**
Instead of a form, I add the payload to the end of the URL after a `#` symbol. I then scan the page's JavaScript code for dangerous functions like `document.write()`, `innerHTML`, `eval()`, and `location.hash`. If these exist, the page reads from the URL and writes to the page without sanitising — that means the payload would execute. The page `/xss_d/` had 2 out of 11 trigger.

I also added a sanitisation check. If the `<` and `>` in the payload got converted to `&lt;` and `&gt;` in the response, the site properly encoded the input and I mark it as safe.

**One thing I ran into:** When I first generated the report, the XSS payloads were sitting inside the HTML file unescaped, and the browser actually ran them — an alert popup appeared saying "XSS". I fixed this by writing a function that converts `<`, `>`, `&`, `"`, and `'` to their HTML codes before putting anything in the report. So `<script>` becomes `&lt;script&gt;` in the report file and the browser just displays it as text.

All findings saved to `xss_findings.json`.

---

## Week 5 — Authentication and Session Testing

This week I tested the login system and session security — basically checking if someone can break in or steal a logged-in session.

**Test 1 — Weak Credentials**
I made a list of 14 common username/password combinations like `admin/admin`, `admin/password`, `root/root`, `test/test` and tried each one on the login page. For every attempt I open a fresh session and include the CSRF token. If the response doesn't say "Login failed" and doesn't redirect back to the login page, login worked and I flag it as vulnerable. On DVWA, `admin/password` worked — the default password was never changed.

**Test 2 — Brute Force**
Similar to Test 1 but with 25 passwords and a different goal. The point here is not to crack the password — it's to check if the website ever stops me. After each attempt I check if the site returned a 429 status code (too many requests), said "account locked", or said "too many attempts". DVWA never does any of this. That means someone could try millions of passwords and never get blocked — no rate limiting exists.

**Test 3 — Insecure Cookies**
After logging in, the server gives the browser a session cookie called `PHPSESSID`. This cookie is what proves you're logged in. I inspect it and check for three important flags:
- `HttpOnly` — if this is missing, JavaScript can read the cookie, so an XSS attack could steal it
- `Secure` — if this is missing, the cookie gets sent over plain HTTP and someone on the same network could intercept it
- `SameSite` — if this is missing, the cookie can be sent in requests from other websites, making CSRF attacks possible

DVWA's cookie is missing all three flags.

**Test 4 — Session Fixation**
I record the session ID before logging in, then log in, then record it again. A secure site should give you a brand new session ID after login. DVWA keeps the same ID. This is dangerous because an attacker could trick you into using a session ID they know, wait for you to log in, and then use that same ID to access your account.

**Test 5 — Session Hijacking**
I log in as admin and copy the `PHPSESSID` cookie value. Then I open a completely new session that has never logged in, manually set that stolen cookie on it, and try to visit a protected page. If the page loads without asking for a login, hijacking works. On DVWA it does — the server just looks at the cookie and doesn't check anything else.

All findings saved to `auth_findings.json`.

---

## Week 6 — Access Control and IDOR Testing

Access control is about making sure users can only access what they're supposed to. This week I tested whether I could access other people's data or admin pages just by changing things in the URL.

**Test 1 — Horizontal Privilege Escalation**
This is when one user can see another user's data. I logged in as admin and then tried changing the `id` parameter in the URL — `?id=1`, `?id=2`, `?id=3`, `?id=4`, `?id=5`. For each one I checked if "First name" and "Surname" appeared in the response, which would mean user data was returned. The server should check that the logged-in user is only asking for their own data — DVWA doesn't check at all, so all 5 IDs returned data.

**Test 2 — Vertical Privilege Escalation**
This is when a regular user can access admin-only pages. I tried visiting these pages directly just by typing the URL:
- `/security.php`
- `/setup.php`
- `/phpinfo.php`

If the page loads with a 200 response and no "access denied" message, it means there is no role check. A normal user should never be able to reach these pages. On DVWA they're all accessible.

**Test 3 — IDOR (Insecure Direct Object Reference)**
IDOR is when the website uses a database ID directly in the URL and doesn't check if you're allowed to access that ID. I tested IDs 1 through 8 and extracted the data from each response using BeautifulSoup. I also tested if I could change the security level of DVWA by just sending a POST request with `security=low` — on DVWA it works, there's no authorisation check.

All findings saved to `idor_findings.json`.

---

## Week 7 — Report Generator

The report generator reads all four findings files and builds a single HTML report that shows everything in one place.

**How it works:**

1. It checks if each findings file exists and loads it
2. It tags each finding with which module it came from
3. It counts how many Critical, High, Medium, and Low findings there are
4. It builds the HTML page with summary stats, a bar chart, and a table for each module
5. It saves the result as `report.html`

For the bar chart I used pure CSS with `div` heights calculated from the counts — no JavaScript libraries needed.

For the fix column, `sqli_findings.json` and `xss_findings.json` don't save a recommendation field. I added a function that looks at the vulnerability type and assigns the right recommendation automatically based on whether it's Error-Based, UNION-Based, Reflected XSS, Stored XSS, and so on.

Everything from the findings files gets passed through an `escape()` function before going into the HTML. This converts `<` to `&lt;`, `>` to `&gt;`, `&` to `&amp;`, `"` to `&quot;`, and `'` to `&#39;`. This is what stopped the XSS payloads from running in the report.

---

## Final Results

| Module | Critical | High | Medium | Total |
|--------|----------|------|--------|-------|
| SQL Injection | 1 | 2 | 1 | 4 |
| XSS | 0 | 20 | 0 | 20 |
| Authentication | 3 | 2 | 1 | 6 |
| Access Control | 0 | 3 | 1 | 4 |
| **Total** | **4** | **27** | **3** | **34** |

---

## Libraries Used

| Library | What it does in this project |
|---------|------------------------------|
| `requests` | Sends HTTP GET and POST requests, manages login sessions and cookies |
| `beautifulsoup4` | Parses HTML responses to find forms, input fields, CSRF tokens, and user data |

No other external libraries needed. The report is plain HTML and CSS.

---

## What I Learned

The biggest thing was understanding why each vulnerability actually works. SQL injection made sense once I saw the MySQL error appear in the terminal. Session fixation clicked when I saw both session IDs printed side by side and they were identical. The XSS payload executing in my own report was a good reminder that the same rules apply everywhere — output needs to be encoded before it goes into HTML, no exceptions.

The pipeline design worked out well. Because every module reads the same `targets.json` format and writes the same findings JSON format, adding a new test module doesn't require changing anything else.
