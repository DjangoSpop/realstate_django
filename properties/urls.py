from django.urls import path, include
from rest_framework.routers import DefaultRouter
from properties.views import PropertyStatsView, PropertyViewSet

router = DefaultRouter()
router.register(r'', PropertyViewSet)  # Registers PropertyViewSet for CRUD operations

urlpatterns = [
    path('stats/', PropertyStatsView.as_view(), name='property-stats'),  # Statistics endpoint
    path('', include(router.urls)),  # Include routes for PropertyViewSet
]
