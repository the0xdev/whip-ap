# SPDX-FileCopyrightText: 2025 Imran M <imran@imranmustafa.net>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.urls import path
from webfinger import views

urlpatterns = [
    path('.well-know/webfinger', views.webfinger, name="webfinger")
]
