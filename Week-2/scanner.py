import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

target_url = "http://localhost/dvwa/"
visited = set()

results = {
    "urls": [],
    "forms": []
}

def crawl(url):
    if url in visited:
        return
    visited.add(url)

    try:
        response = requests.get(url)
    except:
        return

    soup = BeautifulSoup(response.text, "html.parser")

   
    for link in soup.find_all("a"):
        href = link.get("href")
        if href:
            full_url = urljoin(url, href)
            if "dvwa" in full_url:
                if full_url not in results["urls"]:
                    results["urls"].append(full_url)
                crawl(full_url)


    for form in soup.find_all("form"):
        form_data = {
            "page": url,
            "action": form.get("action"),
            "method": form.get("method"),
            "inputs": []
        }

        for inp in form.find_all("input"):
            form_data["inputs"].append({
                "name": inp.get("name"),
                "type": inp.get("type")
            })

        results["forms"].append(form_data)


crawl(target_url)


with open("output.json", "w") as jf:
    json.dump(results, jf, indent=4)


with open("output.txt", "w") as tf:
    tf.write("=== Discovered URLs ===\n")
    for u in results["urls"]:
        tf.write(u + "\n")

    tf.write("\n=== Forms & Input Fields ===\n")
    for f in results["forms"]:
        tf.write(str(f) + "\n")

print("Scan completed. Results saved to output.txt and output.json")
