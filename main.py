import subprocess
import os
import sys
import time

# ---------------- BASE PATH ---------------- #

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SCANNER_PATH = os.path.join(BASE_DIR, "Week-2", "scanner.py")
SQLI_PATH = os.path.join(BASE_DIR, "Week-3", "sqli_tester.py")
XSS_PATH = os.path.join(BASE_DIR, "Week-4", "xss_tester.py")
AUTH_PATH = os.path.join(BASE_DIR, "Week-5", "auth_session_tester.py")
IDOR_PATH = os.path.join(BASE_DIR, "Week-6", "idor_tester.py")
REPORT_PATH = os.path.join(BASE_DIR, "Week-7", "report_generator.py")


# ---------------- COLOR SYSTEM ---------------- #

class Colors:
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    END = '\033[0m'


# ---------------- BANNER ---------------- #

def banner():

    os.system("cls" if os.name == "nt" else "clear")

    print(Colors.CYAN + Colors.BOLD + """

██╗    ██╗███████╗██████╗ ███████╗ ██████╗ █████╗ ███╗   ██╗██████╗ ██████╗  ██████╗ 
██║    ██║██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗████╗  ██║██╔══██╗██╔══██╗██╔═══██╗
██║ █╗ ██║█████╗  ██████╔╝███████╗██║     ███████║██╔██╗ ██║██████╔╝██████╔╝██║   ██║
██║███╗██║██╔══╝  ██╔══██╗╚════██║██║     ██╔══██║██║╚██╗██║██╔═══╝ ██╔══██╗██║   ██║
╚███╔███╔╝███████╗██████╔╝███████║╚██████╗██║  ██║██║ ╚████║██║     ██║  ██║╚██████╔╝
 ╚══╝╚══╝ ╚══════╝╚═════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝     ╚═╝  ╚═╝ ╚═════╝ 

""" + Colors.END)
    print(Colors.CYAN + "      Web Application Security Testing Tool\n" + Colors.END)

    print(Colors.BLUE + "Target  : DVWA (Localhost)" + Colors.END)
    print(Colors.BLUE + "Engine  : Hybrid AI Vulnerability Scanner" + Colors.END)
    print(Colors.BLUE + "Modules : Scanner | SQL Injection | XSS | Auth | IDOR | Report" + Colors.END)

    print(Colors.CYAN + "=" * 70 + Colors.END + "\n")


# ---------------- MODULE RUNNER ---------------- #

def run_module(name, path):

    if not os.path.exists(path):
        print(Colors.RED + f"[ERROR] {name} not found!" + Colors.END)
        return

    print(Colors.YELLOW + f"\n[+] Running {name}...\n" + Colors.END)

    start = time.time()

    try:
        subprocess.run([sys.executable, path], check=True)

        duration = round(time.time() - start, 2)

        print(Colors.GREEN +
              f"[✔] {name} completed in {duration} seconds.\n"
              + Colors.END)

    except subprocess.CalledProcessError:
        print(Colors.RED + f"[!] {name} failed.\n" + Colors.END)


# ---------------- MENU ---------------- #

def show_menu():

    print(Colors.MAGENTA + """
┌────────────────────────────────────────────┐
│            WebScanPro Control Panel        │
├────────────────────────────────────────────┤
│ 1  → Target Scanning Module                │
│ 2  → SQL Injection Module                  │
│ 3  → XSS Module                            │
│ 4  → Authentication & Session Module       │
│ 5  → IDOR Access Control Module            │
│ 6  → Generate Security Report              │
│ 7  → Run Full Security Scan                │
│ 8  → Exit                                  │
└────────────────────────────────────────────┘
""" + Colors.END)


# ---------------- MAIN ---------------- #

if __name__ == "__main__":

    banner()

    while True:

        show_menu()

        choice = input("Select option ➜ ").strip()

        total_start = time.time()

        if choice == "1":

            run_module("Target Scanning Module", SCANNER_PATH)

        elif choice == "2":

            run_module("SQL Injection Module", SQLI_PATH)

        elif choice == "3":

            run_module("XSS Module", XSS_PATH)

        elif choice == "4":

            run_module("Authentication & Session Module", AUTH_PATH)

        elif choice == "5":

            run_module("IDOR / Access Control Module", IDOR_PATH)

        elif choice == "6":

            run_module("Security Report Generator", REPORT_PATH)

        elif choice == "7":

            print(Colors.CYAN + "\n🚀 Running Full Security Scan...\n" + Colors.END)

            run_module("Target Scanning Module", SCANNER_PATH)
            run_module("SQL Injection Module", SQLI_PATH)
            run_module("XSS Module", XSS_PATH)
            run_module("Authentication & Session Module", AUTH_PATH)
            run_module("IDOR / Access Control Module", IDOR_PATH)
            run_module("Security Report Generator", REPORT_PATH)

            total_end = time.time()

            print(Colors.GREEN + Colors.BOLD +
                  f"\n✔ FULL SECURITY SCAN COMPLETED ({round(total_end - total_start, 2)} seconds)\n"
                  + Colors.END)

        elif choice == "8":

            print(Colors.GREEN + "\nExiting WebScanPro... Stay Secure 🔐\n" + Colors.END)
            break

        else:

            print(Colors.RED + "\nInvalid option. Try again.\n" + Colors.END)