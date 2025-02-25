from django.urls import path
from activitypub import views

urlpatterns = [
    path('object/<uuid:uuid>', views.object, name="object"),
    path('activity/<uuid:uuid>', views.activity, name="activity"),

    path('actor/<uuid:uuid>', views.actor, name="actor"),
    path('actor/<uuid:uuid>/inbox', views.inbox, name="actor-inbox"),
    path('actor/<uuid:uuid>/outbox', views.outbox, name="actor-outbox"),
]
