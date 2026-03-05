import json

def save_report(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"[+] Vulnerability report saved to {filename}")

def save_metadata(pages, filename):
    import json
    with open(filename, "w") as f:
        json.dump(pages, f, indent=4)
    print("[+] Metadata saved successfully!")