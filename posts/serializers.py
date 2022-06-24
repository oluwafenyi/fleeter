
from django.core.cache import cache
from rest_framework import serializers

from .models import Post
from accounts.serializers import UserDisplaySerializer
from accounts.models import User


class PostSerializer(serializers.ModelSerializer):
    creator = UserDisplaySerializer(read_only=True)

    class Meta:
        model = Post
        fields = ("id", "text", "creator", "created", "image")


class PostCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "text", "image")

    def validate(self, attrs):
        if not (attrs.get("text") or attrs.get("image")):
            raise serializers.ValidationError("you must post either text or image")
        return attrs

    def create(self, validated_data):
        creator: User = self.context["request"].user
        new_post = Post.objects.create(**validated_data, creator=creator)
        data = PostSerializer(instance=new_post).data
        for follower in creator.followers.all():
            key = "homefeed:%s" % follower.id
            follower_feed: list = cache.get(key)
            if follower_feed is None:
                continue
            follower_feed.insert(0, data)
            cache.set(key, follower_feed, 60 * 60 * 24)

        # add to user's own feed
        key = "homefeed:%s" % creator.id
        user_feed: list = cache.get(key)
        if user_feed is None:
            return new_post
        user_feed.insert(0, data)
        cache.set(key, user_feed, 60 * 60 * 24)
        return new_post
