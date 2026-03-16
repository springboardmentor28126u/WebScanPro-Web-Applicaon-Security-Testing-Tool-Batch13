from request_handler import RequestHandler
from sql_injection import SQLScanner
from crawler import crawl
from xss import test_xss
import json

from auth_session_test import test_default_credentials
from auth_session_test import simulate_bruteforce
from auth_session_test import check_cookie_security
from auth_session_test import test_session_fixation


def main():

    base_url = "http://127.0.0.1/dvwa/"

    print("[*] Web Scan Pro Starting...")

    request_handler = RequestHandler()

    if not request_handler.login(base_url):
        print("[-] Login failed.")
        return

    print("[+] Login successful!")

    request_handler.set_security_low(base_url)

    forms = crawl(base_url, request_handler)

    scanner = SQLScanner(request_handler.session)

    vulnerabilities = []

    # SQL Injection Testing
    for form in forms:
        if form["method"] and form["method"].lower() == "get":

            for input_field in form["inputs"]:

                if input_field["type"] == "text" and input_field["name"]:

                    vulns = scanner.test_get_parameter(
                        form["page"],
                        input_field["name"]
                    )

                    vulnerabilities.extend(vulns)


    # XSS Testing
    for form in forms:

        xss_vulns = test_xss(request_handler, form)

        vulnerabilities.extend(xss_vulns)


    # Authentication Testing

    vulnerabilities.extend(
        test_default_credentials(base_url, request_handler)
    )

    vulnerabilities.extend(
        simulate_bruteforce(base_url, request_handler)
    )

    vulnerabilities.extend(
        check_cookie_security(request_handler)
    )

    vulnerabilities.extend(
        test_session_fixation(base_url, request_handler)
    )


    final_report = {
        "total_forms": len(forms),
        "forms": forms,
        "total_vulnerabilities": len(vulnerabilities),
        "vulnerabilities": vulnerabilities
    }


    with open("scan_results.json", "w") as f:
        json.dump(final_report, f, indent=4)


    print("\nScan Completed Successfully!")
    print(json.dumps(final_report, indent=4))


if __name__ == "__main__":
    main()