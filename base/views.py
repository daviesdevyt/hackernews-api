from collections import OrderedDict
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
    d = serializer.data
    d.append(OrderedDict({"has_next": page_object.has_next()})) # adds a has_next variable to the data sent to help pagination on the frontend
    return Response(d)


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
        paginator = DjangoPaginator(data, 5)
        page_object = paginator.get_page(request.GET.get("page"))
        serializer = serializer_model(page_object, many=True)
        d = serializer.data
        d.append(OrderedDict({"has_next": page_object.has_next(), "has_previous": page_object.has_previous(), "page_count":page_object.paginator.num_pages})) # adds a has_next variable to the data sent to help pagination on the frontend
        return Response(d)
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
        d = serializer.data
        d.append(OrderedDict({"has_next": page_object.has_next()})) # adds a has_next variable to the data sent to help pagination on the frontend
        return Response(d)
    return Response()

@api_view(["GET"])
def index(request):
    return Response()

@api_view(["POST"])
def add_item(request):
    item_types = ["comment", "story", "job", "pollopt", "poll"]
    object_models = {"comment": Comment, "pollopt":PollOption, "post":Post}
    model_serializers = {"comment": CommentSerializer, "pollopt":PollOptionSerializer, "post":PostSerializer}
    item_type = request.data.get("item")
    if item_type not in item_types:
        return Response("Bad request: Invalid type", status=400)
    elif item_type not in object_models:
        model = "post"
    else:
        model = item_type
    
    model_obj = object_models[model]
    model_serializer = model_serializers[model]

    # Clean up the data
    data = dict(request.data)

    del data["item"]

    for i in data.copy():
        data[i] = data[i][0] # Fixes issues with the default request.data QueryDict
        if data[i] == "":    # Remove empty values
            del data[i]
    
    data["type"] = item_type # Set the item type

    if data.get("time"):
        data["time"] = datetime.fromisoformat(request.data['time'])

    if data.get("dead"): # Dead comes as "on" or "None"
        data["dead"] = True

    if model != "post":
        if request.data.get("post"):
            post = Post.objects.filter(id=int(data["post"])).first()
            if not post:
                return Response("Post id doesnt exist", status=404)
            else:
                data['post'] = post
        else:
            return Response("Bad request: "+item_type+" must have a post id", status=400)
    
    # Try saving the data
    try:
        obj = model_obj.objects.create(**data)
        serializer = model_serializer(obj)
    except Exception as e:
        return Response("Bad request: "+str(e), status=400)

    return Response(serializer.data)

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