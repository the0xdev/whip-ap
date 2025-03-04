# SPDX-FileCopyrightText: 2025 Imran M <imran@imranmustafa.net>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.forms import ModelForm
from app.models import Object, Actor
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ActorForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username', 'email', 'password1', 'password2']

class ObjectForm(ModelForm):
    class Meta:
         model = Object
         fields = ["source"]
