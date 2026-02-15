import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

TARGET_URL = "http://localhost:8080"

session = requests.Session()# creates a ession object to maintain all login cookies

# Step 1: Login
# Step 1: Get login page
login_page = session.get(TARGET_URL + "/login.php")

soup = BeautifulSoup(login_page.text, "html.parser")

# Step 2: Extract token
token = soup.find("input", {"name": "user_token"})["value"]

# Creates a dictionary with login credentials.
login_data = {
    "username": "admin",
    "password": "password",
    "user_token": token,
    "Login": "Login"
}

session.post(TARGET_URL + "/login.php", data=login_data)#Sends POST request to login.Logs into the website

print("Login attempted!")


session.post(TARGET_URL + "/login.php", data=login_data)

visited = set()#Tracks visited pages
all_links = []

def crawl(url):#Defines recursive crawling function.
    if url in visited:#Stops crawling if page already scanned
        return

    print("Crawling:", url)
    visited.add(url)
    all_links.append(url)

    response = session.get(url)#Loads the webpage.
    soup = BeautifulSoup(response.text, "html.parser")#parses html content

    for link in soup.find_all("a"):#These represent hyperlinks.anchor tag
        href = link.get("href")#Gets URL from anchor tag
        if href:
            full_url = urljoin(url, href)#converts relative links to absolute URLs

            if TARGET_URL in full_url:
                crawl(full_url)

crawl(TARGET_URL)

results = {
    "target_url": TARGET_URL,
    "total_links_found": len(all_links),
    "links": all_links
}

with open("scan_results.json", "w") as f:
    json.dump(results, f, indent=4)

print("Crawling finished!")
