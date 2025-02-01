import requests
import json

def check_malicious_url(api_key, url):
    # Google Safe Browsing API endpoint
    api_url = "https://safebrowsing.googleapis.com/v4/threatMatches:find"
    
    # Request headers
    headers = {
        "Content-Type": "application/json",
    }
    
    # Request body
    payload = {
        "client": {
            "clientId": "your-client-name",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [
                {"url": url}
            ]
        }
    }

    try:
        response = requests.post(
            f"{api_url}?key={api_key}",
            headers=headers,
            data=json.dumps(payload)
        )
        response.raise_for_status()
        
        result = response.json()
        
        if result.get('matches'):
            return True, result['matches']
        return False, None
    
    except requests.exceptions.RequestException as e:
        print(f"Error checking URL: {e}")
        return None, None

if __name__ == "__main__":
    API_KEY = "YOUR_API_KEY"  # Replace with your API key
    url = input("Enter URL to check: ").strip()
    
    is_malicious, details = check_malicious_url(API_KEY, url)
    
    if is_malicious is None:
        print("Could not complete check due to error")
    elif is_malicious:
        print("⚠️  WARNING: Malicious URL detected! ⚠️")
        print("Threat details:")
        for match in details:
            print(f"Type: {match['threatType']}")
            print(f"Platform: {match['platformType']}")
    else:
        print("✅ URL appears safe")