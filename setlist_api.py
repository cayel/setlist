import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('SETLIST_API_KEY')

def get_attended_events(page):
    url = f"https://api.setlist.fm/rest/1.0/user/IchabodCrane/attended?p={page}"

    payload = {}
    headers = {
        'x-api-key': API_KEY,
        'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    return data

def get_user_info(user_name):
    url = f"https://api.setlist.fm/rest/1.0/user/{user_name}"

    payload = {}
    headers = {
        'x-api-key': API_KEY,
        'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    return data