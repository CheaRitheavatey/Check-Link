# Check-Link
goal: check if a link has any malicious content or is a phishing link

=> input: link 
=> output: boolean

- method 1: use api from Google Safe Browsing
    - input url
    - send that url to google api
    - get the response



1. get api key from google:
    - go to Google Cloud Platform: https://console.developers.google.com/?hl=HU

    - go to APIs & Services or their Library >
    - search for "Safe Browsing API" > click enable
    - create credentials > copy the api key

2. create a function to check if a link is malicious
    - have google safe browsing api endpoint "https://safebrowsing.googleapis.com/v4/threatMatches:find"

    - set http headers:
        - Content-Type: application/json
        - (specify the content type) this tell api that we are going to send json data (structured text)

    - request payload: this code can be find in google safe browsing api docs

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


    - send request to google safe browsing api
    response = requests.post(
    f"{api_url}?key={api_key}", headers=headers, json=payload
    )

    - handling api response by: response.raise_for_status()
    if the request fail it will stop the program 

    - convert response to dictionary
    result = response.json()



    

