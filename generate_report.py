import json
import os

# Open output file properly
with open("output.txt", "w", encoding="utf-8") as output_file:

    output_file.write("=====================================\n")
    output_file.write("        WebScanPro Final Report\n")
    output_file.write("=====================================\n\n")

    # ---------------------------------
    # Milestone 1 - Target Scanning
    # ---------------------------------

    if os.path.exists("scan_results.json"):

        with open("scan_results.json", "r", encoding="utf-8") as f:
            scan_data = json.load(f)

        output_file.write("========== MILESTONE-1 ==========\n")
        output_file.write("Target Scanning Results\n\n")

        for url, forms in scan_data.items():
            output_file.write(f"Page URL: {url}\n")

            for form in forms:
                output_file.write(
                    f"  Form Action: {form.get('form_action', 'N/A')}\n"
                )
                output_file.write(
                    f"  Method: {form.get('method', 'N/A')}\n"
                )
                output_file.write("  Inputs:\n")

                for input_field in form.get("inputs", []):
                    output_file.write(
                        f"     - {input_field.get('name', 'N/A')} "
                        f"({input_field.get('type', 'N/A')})\n"
                    )

                output_file.write("\n")

    else:
        output_file.write("scan_results.json not found.\n\n")

    # ---------------------------------
    # Milestone 2 - SQL Injection
    # ---------------------------------

    if os.path.exists("sqli_report.json"):

        with open("sqli_report.json", "r", encoding="utf-8") as f:
            sqli_data = json.load(f)

        output_file.write("========== MILESTONE-2 ==========\n")
        output_file.write("SQL Injection Findings\n\n")

        for item in sqli_data:
            output_file.write(f"URL: {item['url']}\n")
            output_file.write(f"Payload: {item['payload']}\n")
            output_file.write(f"Severity: {item['severity']}\n")
            output_file.write("---------------------------------\n")

        output_file.write("\n")

    else:
        output_file.write("sqli_report.json not found.\n\n")

    # ---------------------------------
    # Milestone 2 - XSS
    # ---------------------------------

    if os.path.exists("xss_report.json"):

        with open("xss_report.json", "r", encoding="utf-8") as f:
            xss_data = json.load(f)

        output_file.write("XSS Findings\n\n")

        for item in xss_data:
            output_file.write(f"URL: {item['url']}\n")
            output_file.write(f"Payload: {item['payload']}\n")
            output_file.write(f"Severity: {item['severity']}\n")
            output_file.write("---------------------------------\n")

        output_file.write("\n")

    else:
        output_file.write("xss_report.json not found.\n\n")

    output_file.write("Scan Completed Successfully.\n")

print("✅ Final Combined output.txt generated successfully!")