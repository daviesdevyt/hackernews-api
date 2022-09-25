from django.db import models

# Create your models here.
class Post(models.Model):
    id = models.IntegerField(primary_key=True)
    deleted = models.BooleanField(default=False)
    type = models.CharField(max_length=20)
    by = models.CharField(max_length=100, null=True, blank=True)
    time = models.DateTimeField(max_length=100, null=True, blank=True)
    dead = models.BooleanField(max_length=100, null=True, blank=True)
    
    text = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=150, null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    descendants = models.IntegerField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)


class Comments(models.Model):
    text = models.TextField()
    parent = models.ForeignKey(Post, on_delete=models.CASCADE)

class PollOption(models.Model):
    parent = models.IntegerField(null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)