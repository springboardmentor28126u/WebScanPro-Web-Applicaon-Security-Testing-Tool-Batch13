import subprocess
import os
import sys
import time

# ---------------- BASE PATH ---------------- #

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SCANNER_PATH = os.path.join(BASE_DIR, "Week-2", "scanner.py")
SQLI_PATH = os.path.join(BASE_DIR, "Week-3", "sqli_tester.py")
XSS_PATH = os.path.join(BASE_DIR, "Week-4", "xss_tester.py")

# ---------------- COLOR SYSTEM ---------------- #

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


# ---------------- UI FUNCTIONS ---------------- #

def banner():
    os.system("cls" if os.name == "nt" else "clear")

    print(Colors.CYAN + "=" * 70 + Colors.END)
    print(Colors.BOLD + Colors.BLUE +
          "        🛡  WebScanPro - AI Powered Security Scanner  🛡"
          + Colors.END)
    print(Colors.CYAN + "=" * 70 + Colors.END)
    print(Colors.GREEN + "   Target Environment : DVWA (Localhost)" + Colors.END)
    print(Colors.GREEN + "   Modules : Scanner | SQLi (AI) | XSS (AI)" + Colors.END)
    print(Colors.CYAN + "=" * 70 + Colors.END + "\n")


def run_module(name, path):
    print(Colors.YELLOW if hasattr(Colors, "YELLOW") else Colors.WARNING)
    print(f"\n[+] Starting {name}...\n" + Colors.END)

    if not os.path.exists(path):
        print(Colors.RED + f"[!] ERROR: {name} not found!" + Colors.END)
        return False

    start_time = time.time()

    try:
        subprocess.run([sys.executable, path], check=True)
    except subprocess.CalledProcessError:
        print(Colors.RED + f"[!] {name} failed." + Colors.END)
        return False

    end_time = time.time()

    print(Colors.GREEN +
          f"\n[✔] {name} completed in {round(end_time - start_time, 2)} seconds."
          + Colors.END)
    return True


def show_menu():
    print(Colors.BOLD + "Select an option:\n" + Colors.END)
    print("  1️⃣  Run Target Scanner")
    print("  2️⃣  Run SQL Injection Module (AI)")
    print("  3️⃣  Run XSS Module (AI)")
    print("  4️⃣  Run Full Security Scan")
    print("  5️⃣  Exit\n")


# ---------------- MAIN ---------------- #

if __name__ == "__main__":

    banner()

    while True:
        show_menu()
        choice = input("Enter your choice (1-5): ").strip()

        total_start = time.time()

        if choice == "1":
            run_module("Target Scanner Module", SCANNER_PATH)

        elif choice == "2":
            run_module("SQL Injection Module (AI)", SQLI_PATH)

        elif choice == "3":
            run_module("XSS Module (AI)", XSS_PATH)

        elif choice == "4":
            print(Colors.CYAN + "\n🚀 Running Full AI Security Scan...\n" + Colors.END)

            run_module("Target Scanner Module", SCANNER_PATH)
            run_module("SQL Injection Module (AI)", SQLI_PATH)
            run_module("XSS Module (AI)", XSS_PATH)

            total_end = time.time()

            print(Colors.CYAN + "=" * 70 + Colors.END)
            print(Colors.BOLD + Colors.GREEN +
                  " ✅ FULL SECURITY SCAN COMPLETED SUCCESSFULLY"
                  + Colors.END)
            print(Colors.CYAN + "=" * 70 + Colors.END)

            print(Colors.BLUE +
                  f" ⏱ Total Execution Time: {round(total_end - total_start, 2)} seconds"
                  + Colors.END)

            print("\n 📂 Results Generated:")
            print("    → Week-2/output.json")
            print("    → Week-3/sqli_results.json")
            print("    → Week-4/xss_results.json")
            print(Colors.CYAN + "=" * 70 + Colors.END + "\n")

        elif choice == "5":
            print(Colors.GREEN + "\nExiting WebScanPro... Stay Secure 🔐\n" + Colors.END)
            break

        else:
            print(Colors.RED + "\nInvalid choice. Try again.\n" + Colors.END)