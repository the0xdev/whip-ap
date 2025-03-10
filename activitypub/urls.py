# SPDX-FileCopyrightText: 2025 Imran M <imran@imranmustafa.net>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.urls import path
from activitypub import views
from app.models import Object

urlpatterns = [
    path('object/<uuid:uuid>', views.object, name="object"),

    path('activity/<uuid:uuid>', views.activity, name="activity"),

    path('actor/<uuid:uuid>', views.actor, name="actor"),
    path('actor/<uuid:uuid>/inbox', views.inbox, name="actor-inbox"),
    path('actor/<uuid:uuid>/outbox', views.outbox, name="actor-outbox"),
]
