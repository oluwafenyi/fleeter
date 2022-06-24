
from django.core.cache import cache
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

from . import serializers
from .models import User
from .permissions import IsAccountOwner
from core import schemas
from posts.serializers import PostSerializer
from posts.models import Post


class AccountsViewSet(CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()

    @property
    def paginator(self):
        self._paginator = super().paginator
        if self.action in ('account_by_username', 'me', 'my_home_feed'):
            self._paginator = None
        return self._paginator

    def get_permissions(self):
        if self.action == "following":
            return [permissions.IsAuthenticated(), IsAccountOwner()]
        elif self.action in ("me", "my_home_feed"):
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.UserRegistrationSerializer
        elif self.action == "following":
            return serializers.UserFollowingSerializer

    @swagger_auto_schema(request_body=serializers.UserRegistrationSerializer, responses={"201": serializers.UserDisplaySerializer, "400": schemas.bad_request})
    def create(self, request, *args, **kwargs):
        serializer = serializers.UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_user = serializer.save()
        model_serializer = serializers.UserDisplaySerializer(new_user)
        return Response(model_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(methods=["POST", "DELETE"], request_body=serializers.UserFollowingSerializer, responses={"200": schemas.following_response, "400": schemas.bad_request})
    @action(methods=["POST", "DELETE"], detail=True, url_path="following", url_name="following")
    def following(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = serializers.UserFollowingSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        if request.method == "POST":
            serializer.save(follow=True)
            return Response({"following": True})
        else:
            serializer.save(follow=False)
            return Response({"following": False})

    @swagger_auto_schema(methods=["GET"], responses={"200": PostSerializer(many=True)})
    @action(methods=["GET"], detail=True, url_path="posts", url_name="posts")
    def posts(self, request, *args, **kwargs):
        instance = self.get_object()
        queryset = Post.objects.filter(creator=instance).all()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(methods=["GET"], responses={"200": serializers.UserDisplaySerializer(many=True), "404": schemas.not_found})
    @action(methods=["GET"], detail=False, url_path="by/username/(?P<username>[^/.]+)", url_name="by-username")
    def account_by_username(self, request, username, *args, **kwargs):
        try:
            user = User.objects.get(username__iexact=username)
        except User.DoesNotExist:
            return Response({"detail": "resource not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializers.UserDisplaySerializer(user).data)

    @swagger_auto_schema(methods=["GET"], responses={"200": serializers.UserDisplaySerializer(many=True)})
    @action(methods=["GET"], detail=False, url_path="me", url_name="me")
    def me(self, request, *args, **kwargs):
        user = request.user
        return Response(serializers.UserDisplaySerializer(user).data)

    @swagger_auto_schema(methods=["GET"], responses={"200": PostSerializer(many=True)})
    @action(methods=["GET"], detail=False, url_path="me/home-feed", url_name="my-home-feed")
    def my_home_feed(self, request, *args, **kwargs):
        user = request.user
        key = "homefeed:%s" % user.id
        content = cache.get(key)
        if content is None:
            queryset = Post.objects.filter(creator__in=list(user.following.all()) + [request.user]).order_by("-created")
            content = list(PostSerializer(queryset, many=True).data)
            cache.set(key, content, 60 * 60 * 24)
        return Response(content)
