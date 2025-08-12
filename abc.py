import requests
import urllib3

# Suppress the SSL warning in console
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://your-server-ip-or-domain:8443/your-endpoint"
payload = {"key": "value"}  # optional

# GET request ignoring SSL errors
response = requests.get(url, verify=False)
print("GET Response:", response.text)

# POST request ignoring SSL errors
response = requests.post(url, json=payload, verify=False)
print("POST Response:", response.text)
