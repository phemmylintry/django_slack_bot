from django.contrib.auth.models import User
from django.db import models


class MessageData(models.Model):
    text_message = models.TextField()
    file_message = models.TextField(default=None, null=True)
    timestamp = models.DateTimeField(default=None)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    related_action = models.CharField(max_length=100, default=None)
