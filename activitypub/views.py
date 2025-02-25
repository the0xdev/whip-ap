from django.http import HttpResponseNotAllowed, JsonResponse
from django.urls import reverse
from app.models import Object


def object(request, uuid):
    match request.method:
        case "GET":
            obj = Object.objects.get(id=uuid)
            return JsonResponse({
                "@context": "https://www.w3.org/ns/activitystreams",
                "type": "Note",
                "id": reverse("object", args=[uuid]),
                #"attachment": "",
                "attributedTo": obj.attributedTo,
                #"audience": "",
                "content": obj.content,
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
