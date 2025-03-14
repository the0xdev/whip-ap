# SPDX-FileCopyrightText: 2025 Imran M <imran@imranmustafa.net>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render, get_object_or_404, get_list_or_404
from django.urls import reverse
from app.models import Activity, Object
from app.forms import ObjectForm

def htmx(request):
    if request.htmx:
        params = request.GET
        match params['func']:
            case 'obj':
                context = {
                    "obj": get_object_or_404(Object, id=params['id']),
                }
                return render(request, 'app/obj.html', context)
            case 'obj-list':
                obj = get_list_or_404(Object, id=params['id'])
                return render(request, 'app/obj.html', obj)
            case 'update':
                obj = get_object_or_404(Object, id=params['id'])
                context = {
                    "id": obj.id,
                    "form": ObjectForm(
                        instance=obj
                    ),
                    "outbox": reverse('actor-outbox', args=[obj.attributedTo.actor.uuid])
                }
                return render(request, 'htmx/update.html', context)
            case _:
                pass
    else:
        return HttpResponseBadRequest()
