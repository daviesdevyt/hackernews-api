import requests

base_url = "https://hacker-news.firebaseio.com"

def make_request(method, url, **kwargs):
    res = requests.request(method, base_url+url, **kwargs)
    if res.status_code == 200:
        return res.json()
    return None

def get_latest(n):
    max_id = get_max_id()
    return [ max_id-i for i in range(n) ]

def get_item(id):
    return make_request("get", f"/v0/item/{id}.json")

def get_max_id():
    return make_request("GET", "/v0/maxitem.json")