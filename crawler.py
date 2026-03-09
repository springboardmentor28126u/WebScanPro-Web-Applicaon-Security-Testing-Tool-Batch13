import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

session = requests.Session()

base_url = "http://localhost:8080"
login_url = base_url + "/login.php"

visited_urls = set()# keeps track of pages already visited
target_data = []# stores details of forms and their inputs for later use in attack phase


def login():
    print("Logging into DVWA...")

    # Step 1: get login page to extract token
    res = session.get(login_url)
    soup = BeautifulSoup(res.text, "html.parser")# covert html to readable format

    token = soup.find("input", {"name": "user_token"})
    if token:
        token = token.get("value")
    # login form data 
    data = {  
        "username": "admin",
        "password": "password",
        "Login": "Login",
        "user_token": token
    }
    #sending the login request as we used session (cookies are stored)
    session.post(login_url, data=data)

    print("Login complete.")

#function that visits and scans 
def crawl(url):
    if url in visited_urls:
        return

    print("Crawling:", url)
    visited_urls.add(url)

    try:
        res = session.get(url)# opeaning the page using logged in session
    except:
        return

    soup = BeautifulSoup(res.text, "html.parser")

    # -------- Find forms --------
    forms = soup.find_all("form")

    for form in forms:
        form_details = {}

        action = form.get("action")
        method = form.get("method", "get").lower()

        form_details["page"] = url
        form_details["action"] = urljoin(url, action)# where to send the url
        form_details["method"] = method #how the data is sent 
        form_details["inputs"] = []

        inputs = form.find_all("input")

        for input_tag in inputs:
            name = input_tag.get("name")
            input_type = input_tag.get("type", "text")

            form_details["inputs"].append({
                "name": name,
                "type": input_type
            })

        target_data.append(form_details)

    # -------- Find links --------
    links = soup.find_all("a")

    for link in links:
        href = link.get("href")

        if href:
            full_url = urljoin(url, href)

            if base_url in full_url:
                crawl(full_url)


login()
crawl(base_url)

with open("targets.json", "w") as f:
    json.dump(target_data, f, indent=4)

print("\nCrawling complete. Data saved to targets.json")