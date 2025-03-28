# SPDX-FileCopyrightText: 2025 Imran M <imran@imranmustafa.net>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from http.client import HTTPResponse
from django.db.models import ObjectDoesNotExist
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed, JsonResponse, HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.urls import reverse
from app.models import Activity, Object, Actor
import markdown
import re
from urllib.parse import urlparse

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
    act = get_object_or_404(Actor, uuid=uuid)
    return JsonResponse({
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "actor",
        "id": reverse("actor-outbox", args=[act.uuid]),
    })
    

def outbox(request, uuid):
    actor = get_object_or_404(Actor, uuid=uuid)
    print(request.body)
    match request.method:
        case "POST":
            if content_type_check(request.content_type):
                try:
                    obj = check_obj(request.POST.get('object'))
                except Exception as e:
                    print(e)
                    return HttpResponseBadRequest()
                print(obj)
                match request.POST.get('type'):
                    case "Create":
                        pass
                    case "Update":
                        pass
                    case "Delete":
                        obj.entomb()
                        activity = Activity.objects.create(
                            type="Delete",
                            actor=request.user,
                            object=reverse("object", args=[obj.id])
                        )
                        return HttpResponse(status=200)
                    case "Follow":
                        pass
                    case "Add":
                        pass
                    case "Remove":
                        pass
                    case "Like" | "Announce":
                        pass
                    case "Block":
                        pass
                    case "Undo":
                        pass
                    case _:
                        return HttpResponseBadRequest() 
            else:
                return HttpResponseBadRequest() 
        case "GET":
            activity = get_list_or_404(Activity, actor=actor.id)
            print(request.content_type)
            return JsonResponse(
                {
                    "@context": "https://www.w3.org/ns/activitystreams",
                    "id": reverse("actor-inbox", args=[actor.uuid]),
                    "type": "OrderedCollection",
                    "totalItems": len(activity),
                    "items": [reverse("activity", args=[a.id]) for a in activity],
                }
            )
        case _:
            return HttpResponseNotAllowed(['GET'], b"bad")


def content_type_check(content_type):
    return content_type == 'application/ld+json; profile="https://www.w3.org/ns/activitystreams"'or content_type == "application/activity+json" or content_type == "application/x-www-form-urlencoded"

def url_lookup(url):
    url = urlparse(url)
    match id_check(url):
        case "Local":
            path = re.search("actor|activity|object", url.path)
            uuid = re.search("[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}", url.path)
            print(path.group())
            print(uuid)
            if uuid and path:
                try:
                    match path.group():
                        case "actor":
                            return Actor.objects.get(uuid=uuid.group())
                        case "activity":
                            return Activity.objects.get(id=uuid.group())
                        case "object":
                            return Object.objects.get(id=uuid.group())
                except:
                    pass 
        case "Federated":
            pass
    raise ValueError()

def check_obj(obj):
    if type(obj) is str: # simple url ref to object
        return url_lookup(obj)
    elif type(obj) is dict: # embedded object

        if type(id := obj.get("id")) is str: # check for object id
            return url_lookup(id)
        elif type(kind := obj.get("type")) is str and type(object := obj.get("object")) is str: # try and find object based on context
            try:
                return Activity.objects.filter(type=kind, object=object).get() # search for activity
            except:
                raise ValueError("object not found")
        else:
            raise ValueError("object not compliant")
    else:
        raise TypeError("no object given.")

def id_check(id):
    # TODO remove the True when this code actually runs on a server
    if True or id.scheme in ["http", "https"] and id.netloc != "" and id.hostname and id.path != "":

        if True:
            return "Local"
        else:
            return "Federated"
    return "Invalid"

def get_obj(url):
    pass


