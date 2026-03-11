import requests
from bs4 import BeautifulSoup

def extract_forms(url):
    forms_data = []
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
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
                if input_tag.get("name")
            ]
        }
        forms_data.append(form_details)

    return forms_data