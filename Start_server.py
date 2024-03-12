import requests

def start_server():
    url = "http://5.104.75.54:3110/get/start_mine"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)