from django.shortcuts import redirect, render
from app.forms import ObjectForm
from app.models import Object

def index(request):
    return render(request, "app/index.html", {
        "ob": Object.objects.latest('id').content,
    })

def signup(request):
    return render(request, "app/signup.html")

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
