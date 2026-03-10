import requests
import json
import difflib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULT_FILE = os.path.join(BASE_DIR, "idor_results.json")

# Example vulnerable endpoint
target_url = "http://localhost/dvwa/vulnerabilities/idor/?id="

results = []


# ---------------- AI RESPONSE SIMILARITY ---------------- #

def similarity_score(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()


# ---------------- IDOR TEST ---------------- #

def test_idor():

    print("\n[*] Starting AI IDOR Scanner...\n")

    try:

        # baseline request
        base = requests.get(target_url + "1")
        base_text = base.text

        for i in range(2, 6):

            url = target_url + str(i)

            r = requests.get(url)

            score = similarity_score(base_text, r.text)

            print(f"[+] Testing ID={i} | Similarity: {score:.2f}")

            # AI logic: if pages are very similar
            if score > 0.90:

                print(f"[VULNERABLE] Possible IDOR detected at ID={i}")

                results.append({
                    "type": "IDOR Vulnerability",
                    "parameter": "id",
                    "tested_value": i,
                    "similarity_score": score,
                    "severity": "High",
                    "recommendation": "Implement proper access control checks"
                })

    except Exception as e:
        print("Error:", e)


# ---------------- SAVE RESULTS ---------------- #

def save_results():

    with open(RESULT_FILE, "w") as f:
        json.dump(results, f, indent=4)

    print("\n[+] Results saved to idor_results.json")


# ---------------- RUN MODULE ---------------- #

def run_idor_tests():

    print("===================================")
    print(" AI Access Control & IDOR Scanner ")
    print("===================================")

    test_idor()

    save_results()


# ---------------- MAIN ---------------- #

if __name__ == "__main__":
    run_idor_tests()