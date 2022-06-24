
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model


User = get_user_model()


def file_upload_destination(instance, filename):
    return "/".join(["fleeter", timezone.now().strftime("%Y-%m-%d"), filename])


class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=280, blank=True)
    image = models.ImageField(upload_to=file_upload_destination, null=True, blank=True)
