from utils.request_handler import RequestHandler
from modules.crawler import WebCrawler

def main():
    # Change this if your DVWA URL is different
    base_url = "http://localhost:8080/dvwa"

    print("[*] Web Scan Pro Starting...")

    # Initialize request handler
    request_handler = RequestHandler()

    # Login to DVWA
    if not request_handler.login(base_url):
        print("[-] Login failed. Exiting.")
        return

    print("[+] Login successful!")

    # Start crawler
    crawler = WebCrawler(request_handler.session)
    crawler.crawl(base_url)

    print("[+] Crawling finished.")

if __name__ == "__main__":
    main()
