from collections import OrderedDict
from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .tasks import get_initial_items
from .serializer import CommentSerializer, PollOptionSerializer, PostSerializer
from .models import PollOption, Post, Comment
from django.db.models import Count
from rest_framework.pagination import DjangoPaginator


get_initial_items.delay() # Celery job to populate db

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
def view_comments(request, id):
    post = Post.objects.get(id=id)
    if not post:
        return Response("Post doesnt exist")
    comments = Comment.objects.filter(post=post).all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def view_polloptions(request, id):
    post = Post.objects.get(id=id)
    if not post:
        return Response("Post doesnt exist")
    pollopts = PollOption.objects.filter(post=post).all()
    serializer = PollOptionSerializer(pollopts, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def view_post(request, id):
    post = Post.objects.get(id=id)
    if not post:
        return Response("Post doesnt exist")
    serializer = PostSerializer(post)
    return Response(serializer.data)

@api_view(["GET"])
def top_posts(request):
    posts = Post.objects.annotate(num_comments=Count("comments")).order_by("-num_comments")[:10]
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

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
        obj = model_obj.objects.create(**data, by_hackernews=False)
        serializer = model_serializer(obj)
    except Exception as e:
        return Response("Bad request: "+str(e), status=400)

    return Response(serializer.data)

@api_view(["POST"])
def edit_item(request):
    if not request.data.get("id"):
        return Response("Id must be provided", status=400)
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

    # Find the item we are to work with
    obj = model_obj.objects.filter(id=int(request.data['id']))
    if not obj.first():
        return Response("Item with that ID does not exist", status=404)
    elif obj.first().by_hackernews:
        return Response("That item was created by hacker news and cannot be edited", status=404)

    # Delete the item if delete is set
    if request.data.get("delete"):
        obj.first().delete()
        return Response(item_type+" with id: "+request.data["id"]+" deleted")

    # Clean up the data
    data = dict(request.data)

    del data["item"]

    for i in data.copy():
        data[i] = data[i][0] # Fixes issues with the default request.data QueryDict
        if data[i] == "":    # Remove empty values
            del data[i]

    if data.get("time"):
        data["time"] = datetime.fromisoformat(request.data['time'])

    if data.get("dead"): # Dead comes as "on" or "None"
        data["dead"] = True
    
    # Try saving the data
    del data["id"]
    obj.update(**data)
    serializer = model_serializer(obj.first())

    return Response(serializer.data)
