import requests
import json

# Set your client key and client secret
client_key = "awy0vwp91pqmaita"
client_secret = "11b844f58ed4f3457e32950d990058ea"

# Generate a client access token
def get_access_token():
    url = "https://open.tiktokapis.com/oauth/access_token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "client_key": client_key,
        "client_secret": client_secret,
        "grant_type": "client_credential"
    }
    response = requests.post(url, headers=headers, data=data)
    try:
        access_token = response.json().get("access_token")
        return access_token
    except json.decoder.JSONDecodeError:
        print("Error decoding JSON response:", response.text)
        return None

# Fetch the most popular trends of the day
def get_popular_trends(access_token):
    url = "https://open.tiktokapis.com/v2/research/trending"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    try:
        trends = response.json().get("data")
        return trends
    except json.decoder.JSONDecodeError:
        print("Error decoding JSON response:", response.text)
        return None

# Example usage
access_token = get_access_token()
if access_token:
    trends = get_popular_trends(access_token)
    if trends:
        print("Today's popular trends on TikTok:")
        for trend in trends:
            print(trend["title"])
    else:
        print("Failed to fetch trending topics.")
else:
    print("Failed to obtain access token.")
