from datetime import datetime
from pytz import timezone
from time import sleep
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import PostSerializer
from . import hackernewsapi
import threading
from .models import PollOption, Post, Comment
from django.db import IntegrityError

# Generator function to get the items
def get_posts(items):
    for item in items:
        data = hackernewsapi.get_item(item)

        # Recursion to add any comments of the news item
        if data.get("kids"):
            del data['kids']

        if data.get("time"):
            data["time"] = datetime.fromtimestamp(data["time"], tz=timezone('UTC'))

        post_type = data['type']
        if post_type in ["comment", "pollopt"]:
            if data.get('parent'):
                parent = Post.objects.filter(id=data['parent']).first()
                data['parent'] = parent if parent else None
            if post_type == "comment":
                Comment.objects.create(**data)
            elif post_type == "pollopt":
                PollOption.objects.create(**data)
            continue

        yield Post(**data)

# Get first 10 posts for testing purposes
try:
    if Post.objects.count() < 10:
        post_ids = hackernewsapi.get_latest(10)
        Post.objects.bulk_create(get_posts(post_ids))
except IntegrityError as e:
    print(e)

# Create your views here.

@api_view(["GET"])
def latest(request):
    latest_posts = Post.objects.all().order_by("-time")
    serializer = PostSerializer(latest_posts, many=True)
    return Response(serializer.data)

def get_data(): #Cron job for every second
    while True:
        max_id = hackernewsapi.get_max_id()
        last_on_db = Post.objects.last().id
        post_ids = hackernewsapi.get_latest(max_id-last_on_db)
        Post.objects.bulk_create(get_posts(post_ids))
        sleep(5*60)

t = threading.Thread(target=get_data, daemon=True)
t.start()