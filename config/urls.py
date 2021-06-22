from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly


schema_view = get_schema_view(
    openapi.Info(title="Cars Ratings", default_version="v1"),
    public=True,
    permission_classes=[IsAuthenticatedOrReadOnly],
    validators=["ssv"],
)

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # type: ignore

urlpatterns += [
    path("/", include("apps.cars.urls")),
]
