# SPDX-FileCopyrightText: 2025 Imran M <imran@imranmustafa.net>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from uuid import uuid4
from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.html import escape
from markdown import markdown 

from django.urls import reverse

class Actor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(unique=True, default=uuid4, editable=False)
    # key  = None

    @property
    def url_id(self):
        return reverse('actor', args=[self.uuid])

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
    attributedTo = models.ForeignKey(User, on_delete=models.CASCADE)
    #audience = None

    content = models.TextField()
    source = models.TextField()
    name = models.TextField(blank=True)
    #Image = None
    inReplyTo = models.URLField(max_length=256, blank=True, editable=False)
    published = models.DateTimeField(auto_now_add=True) 
    #summary = models.TextField(blank=True)
    #tag = None
    updated = models.DateTimeField(auto_now=True) 
    #url = models.URLField(max_length=256, blank=True)

    tomb = models.BooleanField(default=False)

    to = None
    bto = None
    cc = None
    bcc = None

    def save(self, *args, **kwargs):
        self.content = markdown(escape(self.source))
        super(Object, self).save(*args, **kwargs)

    def entomb(self):
        self.source = ""
        self.inReplyTo = ""

        self.tomb = True
        super(Object, self).save()

    def to_obj(self):
        if self.tomb:
            return {
                "@context": "https://www.w3.org/ns/activitystreams",
                "type": "Tombstone",
                "id": reverse("object", args=[self.id]),
                "formertype": "Note",
                "published": obj.published,
                "deleted": obj.updated,
            }
        else:
           return {
               "@context": "https://www.w3.org/ns/activitystreams",
                    "type": "Note",
                    "id": reverse("object", args=[self.id]),
                    #"attachment": "",
                    "attributedTo": reverse("actor", args=[self.attributedTo.actor.uuid]),
                    #"audience": "",
                    "content": self.content,
                    "source": {
                        "content": self.source,
                        "mediaType": "text/markdown"
                    },
                    #"name": "",
                    #"Image": "",
                    #"inReplyTo": obj.inReplyTo,
                    "published": self.published,
                    "updated": self.updated,
                    #"replies": "",
                    #"summary": "",
                    #"tag": "",
                    #"url": "",
                    #"to": "",
                    #"bto": "",
                    #"cc": "",
                    #"bcc": "",
                    "mediaType": "text/html",
           } 
    @property
    def url_id(self):
        return reverse('object', args=[self.id])

class Activity(models.Model):
    activity_type = [
        ("cr", "Create"),
        ("up", "Update"),
        ("de", "Delete"),
        ("fo", "Follow"),
        ("ac", "Accept"),
        ("re", "Reject"),
        ("ad", "Add"),
        ("re", "Remove"),
        ("li", "Like"),
        ("an", "Announce"),
        ("un", "Undo"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    type = models.CharField(
        max_length=2,
        choices=activity_type,
    )
    actor = models.ForeignKey(User, on_delete=models.CASCADE)
    object = models.URLField(max_length=256)

    published = models.DateTimeField(auto_now_add=True) 

    @property
    def url_id(self):
        return reverse('activity', args=[self.id])
