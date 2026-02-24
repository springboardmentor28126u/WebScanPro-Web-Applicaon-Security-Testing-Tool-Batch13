import requests
from bs4 import BeautifulSoup
from scanner.config import LOGIN_URL, USERNAME, PASSWORD

def get_session(login_url=LOGIN_URL, username=USERNAME, password=PASSWORD):
    session = requests.Session()
    r = session.get(login_url)
    # Grab CSRF token if present
    soup = BeautifulSoup(r.text, 'html.parser')
    token = soup.find('input', {'name': 'user_token'})
    data = {'username': username, 'password': password, 'Login': 'Login'}
    if token:
        data['user_token'] = token['value']
    session.post(login_url, data=data)
    session.cookies.set('security', 'low')
    return session