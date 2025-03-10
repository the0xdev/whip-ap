# SPDX-FileCopyrightText: 2025 Imran M <imran@imranmustafa.net>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from http.client import HTTPResponse
from django.db.models import ObjectDoesNotExist
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from app.models import Activity, Object, Actor
import markdown

def object(request, uuid):
    obj = get_object_or_404(Object, id=uuid)
    match request.method:
        case "GET":
            if request.htmx:
                pass
            else:
                return JsonResponse(obj.to_obj())
        case "POST":
            act_type = request.GET.get('type')
            match act_type:
                case "Like" | "Announce":
                    try:
                        interactions = Activity.objects.filter(
                            type=act_type,
                            actor=request.user,
                            object=reverse("object", args=[obj.id])
                        ).latest('published')
                        undos = Activity.objects.filter(
                            type="Undo",
                            actor=request.user,
                            object=reverse("activity", args=[interactions.id])
                        )
                    except ObjectDoesNotExist:
                        interactions = None
                        undos = None

                    if interactions is None or undos:
                        activity = Activity.objects.create(
                            type=act_type,
                            actor=request.user,
                            object=reverse("object", args=[obj.id])
                        )
                    else:
                        activity = Activity.objects.create(
                            type="Undo",
                            actor=request.user,
                            object=reverse("activity", args=[interactions.id])
                        )
                    return redirect('index')
                case _:
                    return HttpResponseBadRequest()
        case "PATCH":
            pass
        case "DELETE":
            if request.user == obj.attributedTo:
                obj.entomb()
                activity = Activity.objects.create(
                    type="Delete",
                    actor=request.user,
                    object=reverse("object", args=[obj.id])
                )
                return HttpResponse()
            else:
                return HttpResponseForbidden()
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
