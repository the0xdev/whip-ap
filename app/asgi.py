# SPDX-FileCopyrightText: 2025 Imran M <imran@imranmustafa.net>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
ASGI config for app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

application = get_asgi_application()
