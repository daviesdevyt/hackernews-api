import requests

base_url = "https://hacker-news.firebaseio.com"

def make_request(method, url, **kwargs):
    res = requests.request(method, base_url+url, **kwargs)
    if res.status_code == 200:
        return res.json()
    return None

def get_new_stories():
    return make_request("get", "/v0/newstories.json")

def get_item(id):
    return make_request("get", f"/v0/item/{id}.json")