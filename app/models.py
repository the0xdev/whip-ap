from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4

class Actor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

class Object(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    content = models.TextField()

class Activity(models.Model):
    pass
