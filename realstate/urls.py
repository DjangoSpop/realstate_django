from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from leads.views import CreateLeadView
from properties.views import PropertyViewSet, PropertyStatsView

router = DefaultRouter()
router.register(r'properties', PropertyViewSet)
# Swagger Schema View
schema_view = get_schema_view(
    openapi.Info(
        title="Real Estate API",
        default_version='v1',
        description="API documentation for the Real Estate application.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="admin@realestate.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin and apps
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),  # Include user app routes
    path('api/properties/', include('properties.urls')),  # Include properties app routes
    # path('api/leads/', include('leads.urls')),  # Include leads app routes
    path('api/', include(router.urls)),  # Property CRUD
    path('api/properties/stats/', PropertyStatsView.as_view(), name='property-stats'),
    path('api/leads/', CreateLeadView.as_view(), name='create-lead'),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    # Swagger & Redoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
