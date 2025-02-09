from django.urls import path
from webfinger import views

urlpatterns = [
    path('.well-know/webfinger', views.webfinger, name="webfinger")
]
