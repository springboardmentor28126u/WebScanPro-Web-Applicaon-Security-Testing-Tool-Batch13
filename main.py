import subprocess
import os
import sys
import time

# ---------------- BASE PATH ---------------- #

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SCANNER_PATH = os.path.join(BASE_DIR, "Week-2", "scanner.py")
SQLI_PATH = os.path.join(BASE_DIR, "Week-3", "sqli_tester.py")

# ---------------- UI FUNCTIONS ---------------- #

def banner():
    print("\n" + "=" * 60)
    print("   🛡  WebScanPro - Web Application Security Tool  🛡")
    print("=" * 60)
    print("   Target: DVWA (Local Testing Environment)")
    print("=" * 60 + "\n")


def run_module(name, path):
    print(f"\n[+] Starting {name}...\n")

    if not os.path.exists(path):
        print(f"[!] ERROR: {name} not found at {path}")
        sys.exit(1)

    start_time = time.time()

    try:
        subprocess.run([sys.executable, path], check=True)
    except subprocess.CalledProcessError:
        print(f"[!] {name} failed.")
        sys.exit(1)

    end_time = time.time()
    print(f"\n[✔] {name} completed in {round(end_time - start_time, 2)} seconds.")


# ---------------- MAIN ---------------- #

if __name__ == "__main__":

    banner()

    total_start = time.time()

    run_module("Target Scanner Module", SCANNER_PATH)
    run_module("SQL Injection Module", SQLI_PATH)

    total_end = time.time()

    print("\n" + "=" * 60)
    print(" ✅ FULL SECURITY SCAN COMPLETED SUCCESSFULLY")
    print("=" * 60)
    print(f" ⏱ Total Execution Time: {round(total_end - total_start, 2)} seconds")
    print("\n 📂 Results Generated:")
    print("    → Week-2/output.json")
    print("    → Week-3/sqli_results.json")
    print("=" * 60 + "\n")
