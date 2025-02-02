import requests
import json

def check_malicious_url(url):    
    # Google Safe Browsing API endpoint
    api_url = "https://safebrowsing.googleapis.com/v4/threatMatches:find"
    
    # Read API key
    with open("api.txt", "r") as f:
        api_key = f.read().strip()

    # Request headers
    headers = {"Content-Type": "application/json"}
    
    # Request body
    payload = {
        "client": {
            "clientId": "your-client-name",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": [
                "MALWARE", "SOCIAL_ENGINEERING", 
                "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"
            ],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }

    try:
        response = requests.post(
            f"{api_url}?key={api_key}", headers=headers, json=payload
        )
        response.raise_for_status()  # Raises an HTTPError if status is not 200
        
        # Attempt to parse JSON response
        result = response.json()
        
        if "matches" in result:
            return True, result["matches"]
        return False, None

    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        print(f"Response text: {response.text if 'response' in locals() else 'No response'}")
        return None, None

if __name__ == "__main__":
    while True:
        try:    
            url = input("Enter URL to check: ").strip()
            
            is_malicious, details = check_malicious_url(url)

            if is_malicious is None:
                print("❌ Could not complete check due to an error.")
            elif is_malicious:
                print("⚠️ WARNING: Malicious URL detected! ⚠️")
                print("Threat details:")
                for match in details:
                    print(f"- Type: {match['threatType']}")
                    print(f"  Platform: {match['platformType']}")
            else:
                print("✅ URL appears safe.")
            
            again = input("Do you want to check another link? (y/n): ")

            if again == 'y':
                continue
            else:
                print("Close program") 
                break

        except FileNotFoundError:
            print("❌ Error: API key file (api.txt) not found. Make sure it exists.")


