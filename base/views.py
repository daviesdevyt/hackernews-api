from datetime import datetime
from pytz import timezone
from time import sleep
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import hackernewsapi
import threading
from .models import Post

# Generator function to get the items
def get_posts(items):
    for item in items:
        data = hackernewsapi.get_item(item)
        if data['type'] in ["comment", "pollopt"]:
            continue
        if data.get("kids"):
            del data["kids"]
        if data.get("time"):
            data["time"] = datetime.fromtimestamp(data["time"], tz=timezone('UTC'))
        print(data["type"])
        yield Post(**data)

# Get first 10 posts for testing purposes
if Post.objects.count() < 10:
    post_ids = hackernewsapi.get_new_stories()[:3]
    Post.objects.bulk_create(get_posts(post_ids))

# Create your views here.

@api_view(["GET"])
def index(request):
    return Response("Hello world")

def get_data(): #Cron job for every second
    while True:
        sleep(5*60)

t = threading.Thread(target=get_data, daemon=True)
t.start()