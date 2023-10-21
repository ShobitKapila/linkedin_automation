import requests
import json

# Set your LinkedIn API credentials
client_id = "78u4bc5iikwosq"
client_secret = "OML3w76UKlkqXyKd"

# Authenticate with the LinkedIn API
def get_access_token():
    url = "https://www.linkedin.com/developers/apps/214412004/auth"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials", "client_id": client_id, "client_secret": client_secret}
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    access_token = json.loads(response.content)["access_token"]
    return access_token

# Send a message to a LinkedIn user
def send_message(recipient_id, message_body):
    access_token = get_access_token()
    url = "https://api.linkedin.com/v2/messaging/conversations"
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {
        "participants": [recipient_id],
        "message": {
            "body": message_body,
        },
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

# Example usage:

recipient_id = "Kapila Shobit"
message_body = "Hello, world!"

send_message(recipient_id, message_body)
