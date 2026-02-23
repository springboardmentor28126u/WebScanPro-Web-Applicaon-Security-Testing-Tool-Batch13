import requests
from bs4 import BeautifulSoup

print("crawler is started...")

def extract_forms(url):
    forms_data = []
    try:
        response = requests.get(url, timeout=10)  # secure request
        response.raise_for_status()
    except requests.exceptions.SSLError as e:
        print("SSL Error:", e)
        return []
    except Exception as e:
        print("Request failed:", e)
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    forms = soup.find_all("form")

    for form in forms:
        form_details = {
            "action": form.get("action"),
            "method": form.get("method", "get"),
            "inputs": [
                {"type": input_tag.get("type"), "name": input_tag.get("name")}
                for input_tag in form.find_all("input")
            ]
        }
        forms_data.append(form_details)

    return forms_data

url = "https://www.python.org"
forms = extract_forms(url)
print("Extracted forms:", forms)

print("crawler finished...")