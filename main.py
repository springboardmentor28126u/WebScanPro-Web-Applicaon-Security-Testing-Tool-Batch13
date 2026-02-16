from urllib.parse import urlparse
from scanner.crawler import crawl, login_dvwa
from scanner.extractor import extract_forms
from scanner.storage import save_to_json

# Target
target = "http://localhost/dvwa/"
base_domain = urlparse(target).netloc

# Login first
login_dvwa()

# Start crawling
to_visit = [target]
all_pages = set()

while to_visit:
    current = to_visit.pop()
    if current not in all_pages:
        print("Scanning:", current)
        links = crawl(current, base_domain)
        all_pages.add(current)
        to_visit.extend(links)

print("Total pages found:", len(all_pages))

# Extract forms
target_metadata = []

for page in all_pages:
    forms = extract_forms(page)
    page_data = {
        "url": page,
        "forms": forms
    }
    target_metadata.append(page_data)

# Save results
save_to_json(target_metadata)

print("[+] Metadata saved successfully!")
