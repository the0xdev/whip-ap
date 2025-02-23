from django.urls import path
from activitypub import views

urlpatterns = [
    path('object/<uuid:uuid>', views.object, name="object")
]
