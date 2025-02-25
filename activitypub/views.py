from django.http import HttpResponseNotAllowed, JsonResponse
from django.urls import reverse
from app.models import Activity, Object, Actor
import markdown

def object(request, uuid):
    match request.method:
        case "GET":
            obj = Object.objects.get(id=uuid)
            return JsonResponse({
                "@context": "https://www.w3.org/ns/activitystreams",
                "type": "Note",
                "id": reverse("object", args=[uuid]),
                #"attachment": "",
                "attributedTo": reverse("actor", args=[obj.attributedTo.actor.uuid]),
                #"audience": "",
                "content": obj.content,
                "source": {
                    "content": obj.source,
                    "mediaType": "text/markdown"
                },
                #"name": "",
                #"Image": "",
                #"inReplyTo": obj.inReplyTo,
                "published": f"{obj.publishedDate}T{obj.publishedTime}Z",
                #"replies": "",
                #"summary": "",
                #"tag": "",
                #"updated": obj.updated,
                #"url": "",
                #"to": "",
                #"bto": "",
                #"cc": "",
                #"bcc": "",
                "mediaType": "text/html",
                
            })
        case _:
            return HttpResponseNotAllowed(['GET'], b"bad")

def activity(request, uuid):
    match request.method:
        case "GET":
            act = Activity.objects.get(id=uuid)
            print(reverse("object", args=[act.id]))
            return JsonResponse({
                "@context": "https://www.w3.org/ns/activitystreams",
                "type": act.type,
                "id": reverse("activity", args=[act.id]),
                "actor": reverse("actor", args=[act.actor.actor.uuid]),
                "object": act.object,
            })
        case _:
            return HttpResponseNotAllowed(['GET'], b"bad")




def actor(request, uuid):
    match request.method:
        case "GET":
            act = Actor.objects.get(uuid=uuid)
            return JsonResponse({
                "@context": "https://www.w3.org/ns/activitystreams",
                "type": "actor",
                "id": reverse("actor", args=[act.uuid]),
                "inbox": reverse("actor-inbox", args=[act.uuid]),
                "outbox": reverse("actor-outbox", args=[act.uuid]),
            })
        case _:
            return HttpResponseNotAllowed(['GET'], b"bad")



def inbox(request, uuid):
    act = Actor.objects.get(uuid=uuid)
    return JsonResponse({
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "actor",
        "id": reverse("actor-outbox", args=[act.uuid]),
    })

def outbox(request, uuid):
    actor = Actor.objects.get(uuid=uuid)
    activity = Activity.objects.filter(actor=actor.id)
    return JsonResponse({
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": reverse("actor-inbox", args=[actor.uuid]),
        "type": "OrderedCollection",
        "totalItems": len(activity),
        "items": [reverse("activity", args=[a.id]) for a in activity],
    })
