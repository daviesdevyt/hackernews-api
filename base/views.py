from time import sleep
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
import threading

# Create your views here.
def make_request(method, url, **kwargs):
    response = requests.request(method, url, **kwargs)
    if response.status_code == 200:
        return response.json()
    return None

@api_view(["GET"])
def index(request):
    return Response("Hello world")

def get_data(): #Cron job for every second
    while True:
        sleep(5*60)

t = threading.Thread(target=get_data, daemon=True)
t.start()