
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from accounts.models import User


class UserDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "display_name", "username")


class UserRegistrationSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)
    confirm_password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "confirm_password", "display_name")

    def validate(self, data):
        if data.get("password") != data.get("confirm_password"):
            raise serializers.ValidationError({"confirm_password": "passwords do not match"})

        data_copy = data.copy()
        data_copy.pop("confirm_password")

        user = User(**data_copy)

        try:
            validate_password(data["password"], user)
        except ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserFollowingSerializer(serializers.ModelSerializer):
    target_user_id = serializers.IntegerField()

    class Meta:
        model = User
        fields = ["target_user_id"]

    def validate_target_user_id(self, value):
        source_user = self.instance
        try:
            user = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("user does not exist")
        if user == source_user:
            raise serializers.ValidationError("user cannot follow or unfollow theirself")
        return value

    def save(self, follow, **kwargs):
        target_user = User.objects.get(id=self.validated_data["target_user_id"])
        source_user = self.instance
        if follow:
            source_user.follow_user(target_user)
        else:
            source_user.unfollow_user(target_user)

