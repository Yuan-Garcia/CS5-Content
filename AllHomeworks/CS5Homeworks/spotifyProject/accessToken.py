import base64
import requests

client_id = "YOUR CLIENT ID HERE"
client_secret = "YOUR CLIENT SECRET HERE"

# Encode client_id:client_secret in base64
auth_str = f"{client_id}:{client_secret}"
b64_auth_str = base64.b64encode(auth_str.encode()).decode()

# Prepare the headers and payload
headers = {
    'Authorization': f'Basic {b64_auth_str}',
    'Content-Type': 'application/x-www-form-urlencoded'
}

payload = {'grant_type': 'client_credentials'}

# Make the POST request to get the access token
response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=payload)

# Check for successful response
if response.status_code == 200:
    token_data = response.json()
    access_token = token_data['access_token']
    print(f"Access Token: {access_token}")
else:
    print(f"Failed to get access token: {response.status_code}")
    print(f"Response: {response.text}")


