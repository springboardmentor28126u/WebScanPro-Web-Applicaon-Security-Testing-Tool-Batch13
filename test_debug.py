import requests
from bs4 import BeautifulSoup

session = requests.Session()

# Step 1: Get login page
r = session.get("http://localhost/login.php")
print("=== LOGIN PAGE STATUS ===")
print(r.status_code)

# Step 2: Check token
soup = BeautifulSoup(r.text, 'html.parser')
token_tag = soup.find('input', {'name': 'user_token'})
print("=== TOKEN FOUND ===")
print(token_tag)

# Step 3: Try login
token = token_tag['value'] if token_tag else ''
data = {
    'username': 'admin',
    'password': 'password',
    'Login': 'Login',
    'user_token': token
}
resp = session.post("http://localhost/login.php", data=data, allow_redirects=True)
print("=== AFTER LOGIN URL ===")
print(resp.url)
print("=== COOKIES ===")
print(dict(session.cookies))
print("=== RESPONSE SNIPPET ===")
print(resp.text[:500])