from bs4 import BeautifulSoup
from urllib.parse import urljoin

def extract_forms(url, session):
    forms_data = []

    try:
        response = session.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        forms = soup.find_all("form")

        for form in forms:
            form_info = {}

            # Handle relative actions properly
            action = form.get("action")
            full_action = urljoin(url, action) if action else url

            method = form.get("method", "get").lower()

            form_info["action"] = full_action
            form_info["method"] = method
            form_info["inputs"] = []

            for input_tag in form.find_all("input"):
                input_name = input_tag.get("name")
                input_type = input_tag.get("type", "text")

                form_info["inputs"].append({
                    "name": input_name,
                    "type": input_type
                })

            forms_data.append(form_info)

    except Exception as e:
        print(f"Error extracting forms from: {url}")
        print(e)

    return forms_data