import requests
from bs4 import BeautifulSoup
from scanner.config import LOGIN_URL, USERNAME, PASSWORD

def get_session(login_url=LOGIN_URL, username=USERNAME, password=PASSWORD):
    session = requests.Session()

   
    r = session.get(login_url)
    soup = BeautifulSoup(r.text, 'html.parser')

   
    token_tag = soup.find('input', {'name': 'user_token'})
    token = token_tag['value'] if token_tag else ''

    data = {
        'username': username,
        'password': password,
        'Login': 'Login',
        'user_token': token
    }
    login_resp = session.post(login_url, data=data, allow_redirects=True)

    
    session.cookies.set('security', 'low')
    session.cookies.set('PHPSESSID', session.cookies.get('PHPSESSID'))

    verify = session.get("http://localhost:8081/index.php")
    if 'login.php' in verify.url:
        print("  [ERROR] Login failed! Check config.py credentials")
    else:
        print("  [OK] Session active - logged in successfully")

    return session