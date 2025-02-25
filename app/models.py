from uuid import uuid4
from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Actor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    key  = None
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Actor.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.actor.save()

class Object(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    #attachment = None
    attributedTo = models.URLField(max_length=256)
    #audience = None
    content = models.TextField()
    name = models.TextField(blank=True)
    #Image = None
    inReplyTo = models.URLField(max_length=256, blank=True)
    publishedDate = models.DateField(auto_now_add=True) 
    publishedTime = models.TimeField(auto_now_add=True) 
    #summary = models.TextField(blank=True)
    #tag = None
    updatedDate = models.DateField(auto_now=True) 
    updatedTime = models.TimeField(auto_now=True) 
    #url = models.URLField(max_length=256, blank=True)

    to = None
    bto = None
    cc = None
    bcc = None


class Activity(models.Model):
    pass
