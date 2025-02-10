from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.utils.translation import gettext_lazy as _

from .swagger import schema_view

admin.site.site_title = _("Shop Adminstoration")
admin.site.site_header = _("Shop Adminstoration")
admin.site.index_title = _("Shop Adminstoration")
admin.site.site_url = settings.SITE_URL

admin.site.index_template = "admin/dashboard.html"
admin.autodiscover()


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("", include("apps.front_shop.urls")),
    path("api/v1/", include("apps.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
