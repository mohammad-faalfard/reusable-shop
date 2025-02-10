from django.urls import path

from . import views

urlpatterns = [
    path("is-app-messages/", views.UserMessageView.as_view({"get": "list"})),
    path("is-app-messages/<int:id>/", views.UserMessageView.as_view({"get": "retrieve"})),
    path(
        "is-app-messages/<int:id>/seen/",
        views.UserMessageView.as_view({"post": "seen"}),
    ),
    path(
        "is-app-messages/devices/sync/",
        views.UserDeviceView.as_view({"post": "create"}),
    ),
]
