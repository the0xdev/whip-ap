# SPDX-FileCopyrightText: 2025 Imran M <imran@imranmustafa.net>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.db.models import ObjectDoesNotExist
from django.http import HttpResponseBadRequest, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from app.models import Activity, Object, Actor
import markdown

def object(request, uuid):
    match request.method:
        case "GET":
            obj = Object.objects.get(id=uuid)
            if False:
                return JsonResponse({
                    "@context": "https://www.w3.org/ns/activitystreams",
                    "type": "Tombstone",
                    "id": reverse("object", args=[uuid]),
                    "formertype": "Note",

                    "deleted": f"{obj.updatedDate}T{obj.updatedTime}Z",

                })
            else:
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
                    "published": obj.published,
                    "updated": obj.updated,
                    #"replies": "",
                    #"summary": "",
                    #"tag": "",
                    #"url": "",
                    #"to": "",
                    #"bto": "",
                    #"cc": "",
                    #"bcc": "",
                    "mediaType": "text/html",
                    
            })
        case "POST":
            act_type = request.GET.get('type')
            match act_type:
                case "Like" | "Announce":
                    try:
                        interactions = Activity.objects.filter(
                            type=act_type,
                            actor=request.user,
                            object=reverse("object", args=[uuid])
                        ).latest('published')
                        undos = Activity.objects.filter(
                            type="Undo",
                            actor=request.user,
                            object=reverse("activity", args=[interactions.id])
                        )
                        print(interactions)

                        print(undos)
                    except ObjectDoesNotExist:
                        interactions = None
                        undos = None


                    if interactions is None or undos:
                        print("do")
                        activity = Activity.objects.create(
                            type=act_type,
                            actor=request.user,
                            object=reverse("object", args=[uuid])
                        )
                    else:
                        print("undo")
                        activity = Activity.objects.create(
                            type="Undo",
                            actor=request.user,
                            object=reverse("activity", args=[interactions.id])
                        )
                    return redirect("index")

                case "Delete":
                    pass
                case _:
                    return HttpResponseBadRequest()
            pass
        case "PUT":
            pass
        case _:
            return HttpResponseNotAllowed(['GET'], b"bad")

# def activity_create(request):
#     match request.method:
#         case "POST":
#             obj = request.GET.get('obj')
#             act_type = request.GET.get('type')

#             if not obj or not act_type:
#                return HttpResponseBadRequest(b"no object or activity type provided") 
#             match act_type:
#                 case "Announce" | "Like":
#                     activity = Activity.objects.create(
#                         type=act_type,
#                         actor=request.user,
#                         object=reverse("object", args=[obj])
#                     )
#                 case "Undo":
#                     activity = Activity.objects.create(
#                         type=act_type,
#                         actor=request.user,
#                         object=reverse("activity", args=[obj])
#                     )
#                 case _:
#                     return HttpResponseBadRequest(b"invalid activity")

#             return redirect("index")


            
#         case _:
#             return HttpResponseNotAllowed(['GET'], b"bad")


def activity(request, uuid):
    match request.method:
        case "GET":
            act = Activity.objects.get(id=uuid)
            print(reverse("object", args=[act.id]))
            return JsonResponse({
                "@context": "https://www.w3.org/ns/activitystreams",
                "type": act.type,
                "id": reverse("activity", args=[act.id]),
                "published": act.published,
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
