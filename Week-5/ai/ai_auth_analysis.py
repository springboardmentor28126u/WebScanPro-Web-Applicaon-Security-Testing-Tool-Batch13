import json


def analyze_auth_results():

    try:
        with open("../auth_results.json", "r") as f:
            data = json.load(f)

    except:
        print("No auth_results.json found")
        return

    ai_report = []

    for vuln in data:

        if vuln["type"] == "Weak Credentials":

            analysis = {
                "vulnerability": "Weak Authentication",
                "risk": "Attackers can gain unauthorized access using common passwords",
                "recommendation": "Implement strong password policies and account lockout mechanisms",
                "severity": "High"
            }

            ai_report.append(analysis)

        elif vuln["type"] == "Cookie Found":

            analysis = {
                "vulnerability": "Session Cookie Exposure",
                "risk": "Session cookies may be stolen leading to session hijacking",
                "recommendation": "Use Secure, HttpOnly and SameSite cookie flags",
                "severity": "Medium"
            }

            ai_report.append(analysis)

    with open("../ai_report.json", "w") as f:
        json.dump(ai_report, f, indent=4)

    print("[AI] Security analysis generated in ai_report.json")


if __name__ == "__main__":
    analyze_auth_results()