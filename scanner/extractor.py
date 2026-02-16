from bs4 import BeautifulSoup
from urllib.parse import urljoin
from scanner.crawler import session  # Import authenticated session


def extract_forms(url):
    forms_data = []

    try:
        response = session.get(url)  # Use session instead of requests
        soup = BeautifulSoup(response.text, "html.parser")

        forms = soup.find_all("form")

        for form in forms:
            form_info = {}
            form_info["action"] = urljoin(url, form.get("action"))
            form_info["method"] = form.get("method", "get").lower()

            inputs = []
            for input_tag in form.find_all("input"):
                input_data = {
                    "name": input_tag.get("name"),
                    "type": input_tag.get("type", "text")
                }
                inputs.append(input_data)

            form_info["inputs"] = inputs
            forms_data.append(form_info)

        return forms_data

    except Exception as e:
        print("Error extracting forms from:", url)
        return []
