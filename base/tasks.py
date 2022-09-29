from celery import shared_task
from .models import Post, Comment, PollOption
from time import sleep
from . import hackernewsapi
from datetime import datetime
from django.db import IntegrityError, OperationalError
from pytz import timezone


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

@shared_task
def get_initial_items():
    try:
        if Post.objects.count() < 100:
            post_ids = hackernewsapi.get_latest(100)
            get_and_save_items(post_ids)
    except (IntegrityError, OperationalError) as e:
        print(e)

    def latest_on_db():
        last_post = Post.objects.last()
        last_comment = Comment.objects.last()
        last_option = PollOption.objects.last()
        last_post_id = last_post.id if last_post else 0
        last_comment_id = last_comment.id if last_comment else 0
        last_option_id = last_option.id if last_option else 0
        return max(last_post_id, last_comment_id, last_option_id)
        
    while True:
        max_id = hackernewsapi.get_max_id()
        diff = max_id-latest_on_db()
        post_ids = hackernewsapi.get_latest(diff)
        get_and_save_items(post_ids)
        sleep(5*60)

