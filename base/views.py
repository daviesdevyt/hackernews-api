from datetime import datetime
from pytz import timezone
from time import sleep
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import PostSerializer
from . import hackernewsapi
import threading
from .models import PollOption, Post, Comment

# Generator function to get the items
def get_posts(items):
    for item in items:
        data = hackernewsapi.get_item(item)

        # Recursion to add any comments if the news item
        if data.get("kids"):
            if len(data["kids"]) > 0:
                get_posts(data['kids'])            
            del data['kids']

        if data.get("time"):
            data["time"] = datetime.fromtimestamp(data["time"], tz=timezone('UTC'))

        post_type = data['type']
        print(post_type)
        if post_type in ["comment", "pollopt"]:
            if data.get('parent'):
                data['parent'] = Post.objects.get(id=data['parent'])
            if post_type == "comment":
                Comment.objects.create(**data)
            elif post_type == "pollopt":
                PollOption.objects.create(**data)
            return

        yield Post(**data)

# Get first 10 posts for testing purposes
if Post.objects.count() < 10:
    post_ids = hackernewsapi.get_new_stories()[:10]
    Post.objects.bulk_create(get_posts(post_ids))

# Create your views here.

@api_view(["GET"])
def latest(request):
    latest_posts = Post.objects.all().order_by("-time")
    serializer = PostSerializer(latest_posts, many=True)
    return Response(serializer.data)

def get_data(): #Cron job for every second
    while True:
        sleep(5*60)

t = threading.Thread(target=get_data, daemon=True)
t.start()