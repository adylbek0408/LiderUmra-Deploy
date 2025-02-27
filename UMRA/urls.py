from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.i18n import i18n_patterns 

schema_view = get_schema_view(
    openapi.Info(
        title="UMRA API",
        default_version='v1',
        description="API документация для UMRA проекта",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@umra.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    # Non-translated URLs here
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('api/tour/', include('apps.tour.urls')),
    path('api/crm/', include('apps.crm.urls')),
    path('api/blog/', include('apps.blog.urls')),
    prefix_default_language=False,
)

