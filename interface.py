import tkinter as tk
import requests
from main import check_malicious_url

class interface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Check-Link")
        self.root.geometry("300x200")

        self.label = tk.Label(self.root, text="Enter URL to check:")
        self.label.pack()

        self.entry = tk.Entry(self.root)
        self.entry.pack(pady=10)

        # create a frame for 2 button to be next to each other
        self.buttonFrame = tk.Frame(self.root)
        self.buttonFrame.columnconfigure(0,weight=1)
        self.buttonFrame.columnconfigure(1,weight=1)

        self.button = tk.Button(self.buttonFrame, text="Check", command=self.check_url)
        self.button.grid(row=0,column=0,pady=10,sticky=tk.W+tk.E)

        self.clearButton = tk.Button(self.buttonFrame, text="Clear", command=self.close)
        self.clearButton.grid(row=0,column=1,pady=10,sticky=tk.W+tk.E)


        self.buttonFrame.pack()
        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack()
        self.root.mainloop()

    def check_url(self):
        while (self.entry.get() != ""):
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
                    "threatEntries": [{"url": self.entry.get()}]
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
                    threatType = [match['threatType'] for match in result['matches']]
                    return self.result_label.config(text=f"⚠️ WARNING: Malicious URL detected! ⚠️\nThreat Type: {threatType}")

            except requests.exceptions.RequestException as e:
                self.result_label.config(text="❌ Error: Could not complete check due to an error.")
                # print(f"❌ Error: {e}")
                # print(f"Response text: {response.text if 'response' in locals() else 'No response'}")
                # return None, None
                # try:
                #     while (self.entry.get() != ""):
                #         check_malicious_url(self.entry.get())
                #         self.result_label.config(text="✅ URL appears safe.")
                #         break
                #     else:
                #         self.result_label.config(text="Please enter a URL.")
                # except FileNotFoundError:
                #     self.result_label.config(text="❌ Error: API key file (api.txt) not found. Make sure it exists.")
        else:
            self.result_label.config(text="Please enter a URL.")
    def close(self):
        self.entry.delete(0, tk.END)
interface()