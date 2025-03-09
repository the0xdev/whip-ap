# SPDX-FileCopyrightText: 2025 Imran M <imran@imranmustafa.net>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse
from app.forms import ActorForm, ObjectForm
from app.models import Activity, Object

from django.db.models import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm

def index(request):

    try:
        posts = Object.objects.filter(tomb=False)[:20]
    except ObjectDoesNotExist:
        posts = [] 

    context = {
        "posts": posts,
        
    }
    return render(request, "app/index.html", context)

def signup(request):
    context = {
        "form": UserCreationForm(),
    }
    match request.method:
        case "GET":
            return render(request, "app/signup.html", context)
        case "POST":
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect("index")
            else:
                return render(request, "app/signup.html", context)
        case _:
            return redirect("index")


@login_required()
def post(request, **kwargs):
    obj = kwargs["obj"]
    context = {
        "form": ObjectForm()
    }
    match request.method:
        case "GET":
            return render(request, "app/post.html", context)
        case "POST":
            form = ObjectForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.attributedTo = request.user
                obj.source = form.cleaned_data['source']

                activity = Activity.objects.create(
                    type="Create",
                    actor=request.user,
                    object=reverse("object", args=[obj.id])
                )

                obj.save()
                activity.save()
                return redirect("index")
            else:
                return render(request, "app/post.html", context)
        case _:
            return redirect("index")

def profile(request):
    return render(request, "app/profile.html")

def account(request):
    return render(request, "app/account.html")
