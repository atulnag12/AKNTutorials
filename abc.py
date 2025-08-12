import requests
import urllib3

# Suppress the SSL warning in console
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://your-server-ip-or-domain:8443/your-endpoint"
username = "your-username"
password = "your-password"
payload = {"key": "value"}  # optional

# GET request with authentication
response = requests.get(url, auth=(username, password), verify=False)
print("GET Response:", response.text)

# POST request with authentication
response = requests.post(url, json=payload, auth=(username, password), verify=False)
print("POST Response:", response.text)

