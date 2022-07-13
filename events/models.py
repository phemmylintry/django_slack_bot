from django.contrib.auth.models import User
from django.db import models


class MessageData(models.Model):
    text_message = models.TextField()
    file_message = models.FileField(upload_to="files/", blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    related_action = models.CharField(max_length=100, blank=True, null=True)
