from django.contrib.auth import login
from django.shortcuts import redirect, render
from app.forms import ObjectForm, UserRegerstartionForm
from app.models import Object

def index(request):
    return render(request, "app/index.html", {
    })

def signup(request):
    context = {
        "form": UserRegerstartionForm(),
    }
    match request.method:
        case "GET":
            return render(request, "app/signup.html", context)
        case "POST":
            form = UserRegerstartionForm(request.POST)
            if form.is_valid() and form.is_valid():
                user = form.save()
                login(request, user)
                return redirect("index")
            else:
                return render(request, "app/signup.html", context)
        case _:
            return redirect("index")

def post(request):
    context = {"form": ObjectForm()}
    match request.method:
        case "GET":
            return render(request, "app/post.html", context)
        case "POST":
            form = ObjectForm(request.POST)
            if form.is_valid():
                new = form.save()
                return redirect("index")
            else:
                return render(request, "app/post.html", context)
        case _:
            return redirect("index")

def profile(request):
    return render(request, "app/profile.html")

def account(request):
    return render(request, "app/account.html")
