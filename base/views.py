from datetime import datetime
from pytz import timezone
from time import sleep
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import CommentSerializer, PollOptionSerializer, PostSerializer
from . import hackernewsapi
import threading
from .models import PollOption, Post, Comment
from django.db import IntegrityError
from django.db.models import Q
from rest_framework.pagination import DjangoPaginator

# Generator function to get the items
def get_and_save_items(items):
    for item in items:
        data = hackernewsapi.get_item(item)

        if data.get("kids"):
            del data['kids']

        if data.get("time"):
            data["time"] = datetime.fromtimestamp(data["time"], tz=timezone('UTC'))

        post_type = data['type']
        if post_type in ["comment", "pollopt"]:
            if data.get('parent'):
                parent = Post.objects.filter(id=data['parent']).first()
                data['post'] = parent if parent else None
                del data['parent']
            if post_type == "comment":
                Comment.objects.create(**data)
            elif post_type == "pollopt":
                PollOption.objects.create(**data)
            continue

        Post.objects.create(**data)

# Get first 10 posts for testing purposes
try:
    if Post.objects.count() < 10:
        post_ids = hackernewsapi.get_latest(10)
        get_and_save_items(post_ids)
except IntegrityError as e:
    print(e)

# Create your views here.

@api_view(["GET"])
def latest(request):
    latest_posts = Post.objects.all().order_by("-id")
    paginator = DjangoPaginator(latest_posts, 5)
    page_object = paginator.get_page(request.GET.get("page"))
    serializer = PostSerializer(page_object, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def filter_news(request):
    item_type = request.GET.get("type")
    if item_type:
        serializers = {"comment": CommentSerializer, "pollopt":PollOptionSerializer, "post":PostSerializer}
        object_models = {"comment": Comment, "pollopt":PollOption, "post":Post}
        if item_type not in serializers:
            model = "post"
        else:
            model = item_type
        serializer_model = serializers[model]
        type = object_models[model]
        if model == "post":
            data = type.objects.filter(type=item_type).all().order_by('-id')
        else:
            data = type.objects.order_by("-id")
        paginator = DjangoPaginator(data, 4)
        page_object = paginator.get_page(request.GET.get("page"))
        serializer = serializer_model(page_object, many=True)
        return Response(serializer.data)
    return Response()

@api_view(["GET"])
def search(request):
    q = request.GET.get("query")
    if q:
        querys = q.split()
        data = []
        for query in querys:
            data += Post.objects.filter(title__contains=query)
        paginator = DjangoPaginator(data, 4)
        page_object = paginator.get_page(request.GET.get("page"))
        serializer = PostSerializer(page_object, many=True)
        return Response(serializer.data)
    return Response()

@api_view(["GET"])
def index(request):
    return Response()

def get_data(): #Cron job for every second
    def max_on_db():
        last_post = Post.objects.last()
        last_comment = Comment.objects.last()
        last_option = PollOption.objects.last()
        last_post_id = last_post.id if last_post else 0
        last_comment_id = last_comment.id if last_comment else 0
        last_option_id = last_option.id if last_option else 0
        return max(last_post_id, last_comment_id, last_option_id)
        
    while True:
        max_id = hackernewsapi.get_max_id()
        last_on_db = max_on_db()
        post_ids = hackernewsapi.get_latest(max_id-last_on_db)
        get_and_save_items(post_ids)
        sleep(5*60)

t = threading.Thread(target=get_data, daemon=True)
t.start()