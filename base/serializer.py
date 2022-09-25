from rest_framework import serializers
from .models import Post, Comment, PollOption

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
class PollOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollOption
        fields = "__all__"