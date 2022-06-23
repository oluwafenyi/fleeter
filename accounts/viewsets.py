
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


class AccountsViewSet(CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        elif self.action == "following":
            return [permissions.IsAuthenticated(), IsAccountOwner()]

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
