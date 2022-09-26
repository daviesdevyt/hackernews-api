from rest_framework import serializers
from .models import Post, Comment, PollOption

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

class PollOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollOption
        fields = "__all__"

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    poll_options = PollOptionSerializer(many=True)
    class Meta:
        model = Post
        fields = "__all__"