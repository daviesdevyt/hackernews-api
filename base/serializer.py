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
    def __init__(self, instance=None, data=..., **kwargs):
        if isinstance(instance, PollOption):
            self.poll_options = PollOption(many=True)
        super().__init__(instance, data, **kwargs)
    class Meta:
        model = Post
        fields = "__all__"