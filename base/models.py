from django.db import models

# Create your models here.
class Base(models.Model):
    id = models.IntegerField(primary_key=True)
    deleted = models.BooleanField(default=False)
    type = models.CharField(max_length=20)
    by = models.CharField(max_length=100, null=True, blank=True)
    time = models.DateTimeField(max_length=100, null=True, blank=True)
    dead = models.BooleanField(max_length=100, null=True, blank=True)
    class Meta:
        abstract = True

class Post(Base):
    text = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=150, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    descendants = models.IntegerField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)

class Comment(Base):
    text = models.TextField(null=True, blank=True)
    parent = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)

class PollOption(Base):
    order_id = models.IntegerField(default=0)
    score = models.IntegerField(null=True, blank=True)
    parent = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)