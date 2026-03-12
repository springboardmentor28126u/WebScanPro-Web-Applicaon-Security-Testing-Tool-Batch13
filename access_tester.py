import requests

def test_idor(session, base_url):
    print("\n--- [WebScanPro] Starting Week 6: IDOR & Access Control Testing ---")
    
    # Target URL that uses a 'user_id' parameter
    # Note: Adjust the path based on your DVWA structure
    target_path = "vulnerabilities/sqli/" 
    
    # We will try to loop through IDs to see if we can pull multiple user records
    for user_id in range(1, 5):
        test_url = f"{base_url}/{target_path}?id={user_id}&Submit=Submit"
        print(f"[*] Testing IDOR on: {test_url}")
        
        response = session.get(test_url)
        
        # Detection Logic: Check if we see different user data in the response
        if "First name:" in response.text:
            # Extract the name for the report (simple text find)
            start = response.text.find("First name:")
            end = response.text.find("<br", start)
            user_data = response.text[start:end].strip()
            print(f"   [!] SUCCESS: Unauthorized data accessed: {user_data}")
        else:
            print(f"   [-] No data found for ID {user_id}")

# --- EXECUTION ---
# (Assumes you have your 'session' object from your previous auth_tester.py)
# test_idor(session, "http://localhost:8080")