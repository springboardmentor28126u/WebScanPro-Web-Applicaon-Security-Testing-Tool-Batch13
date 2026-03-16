from bs4 import BeautifulSoup
from urllib.parse import urljoin

def crawl(start_url, requester, max_depth=2):
    visited = set()
    queue = [(start_url, 0)]
    forms_data = []

    while queue:
        url, depth = queue.pop(0)

        if url in visited or depth > max_depth:
            continue

        # print(f"Crawling: {url}")
        visited.add(url)

        try:
            response = requester.session.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

            # 🔥 Extract forms
            for form in soup.find_all("form"):
                form_info = {
                    "page": url,
                    "action": form.get("action"),
                    "method": form.get("method"),
                    "inputs": []
                }

                for input_tag in form.find_all("input"):
                    form_info["inputs"].append({
                        "name": input_tag.get("name"),
                        "type": input_tag.get("type")
                    })

                forms_data.append(form_info)

            # Continue crawling links
            for link in soup.find_all("a", href=True):
                full_url = urljoin(url, link["href"])

                if (
                    "/dvwa/" in full_url
                    and "logout.php" not in full_url
                    and full_url not in visited
                ):
                    queue.append((full_url, depth + 1))

        except:
            pass

    return forms_data