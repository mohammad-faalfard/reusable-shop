from django.urls import include, path

urlpatterns = [
    path("account/", include("apps.account.urls")),
    path("base/", include("apps.base.urls")),
    path("messaging/", include("apps.messaging.urls")),
]
