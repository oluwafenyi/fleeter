from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import permissions, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from .models import Post
from .serializers import PostSerializer, PostCreationSerializer
from .permissions import IsPostCreator
from core import schemas


class PostsViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return PostCreationSerializer
        return self.serializer_class

    def get_parsers(self):
        if self.request.method == "POST":
            return [FormParser(), MultiPartParser()]
        return super().get_parsers()

    def get_permissions(self):
        if self.action == "create":
            return [permissions.IsAuthenticated()]
        elif self.action in ["destroy", "media_upload"]:
            return [permissions.IsAuthenticated(), IsPostCreator()]
        return [permissions.AllowAny()]

    @swagger_auto_schema(request_body=PostCreationSerializer, responses={"201": PostSerializer, "400": schemas.bad_request})
    def create(self, request, *args, **kwargs):
        serializer = PostCreationSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(PostSerializer(instance=instance).data, status=status.HTTP_201_CREATED)
