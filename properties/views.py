from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django_ratelimit.decorators import ratelimit
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count  # Explicit import of aggregation functions
from .models import Property, PropertyImage, Location
from .serializers import PropertySerializer


class PropertyViewSet(ModelViewSet):
    """
    A viewset for managing property CRUD operations and filtering.
    """
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['price', 'location__city', 'type', 'bedrooms', 'bathrooms']  # Use correct fields

    def get_queryset(self):
        """
        Extend filtering with query parameters.
        """
        queryset = self.queryset
        listing_type = self.request.query_params.get('listingType')  # Example: "sale" or "rent"
        min_price = self.request.query_params.get('minPrice')  # Example: "100000"
        max_price = self.request.query_params.get('maxPrice')  # Example: "500000"

        if listing_type:
            queryset = queryset.filter(listing_type=listing_type)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset


class PropertyStatsView(APIView):
    """
    View to provide aggregated statistics about properties.
    """

    def get(self, request, *args, **kwargs):
        stats = {
            "total_properties": Property.objects.count(),
            "total_views": Property.objects.aggregate(total_views=Sum('views'))['total_views'] or 0,
            "total_favorites": Property.objects.aggregate(total_favorites=Count('favorites'))['total_favorites'] or 0,
        }
        return Response({"success": True, "data": stats})


class FeaturedPropertiesView(ListAPIView):
    queryset = Property.objects.filter(is_featured=True).order_by('-views')
    serializer_class = PropertySerializer


class PropertyImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, property_id):
        property_obj = Property.objects.get(id=property_id)
        files = request.FILES.getlist("images")

        if len(files) > 10:
            return Response({"sucess": False, "message": "Too many images Max 10 images"}, status=400)
        for file in files:
            PropertyImage.objects.create(property=property_obj, image=file)

        return Response({"sucess": True, "message": "Images saved successfully"}, status=200)


class NearbyPropertiesView(APIView):
    def get(self, request):
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')

        user_location = Point(float(lat), float(lng), srid=4326)
        properties = Property.objects.annotate(distance=Distance('location__coordinates', user_location)).filter(
            distance__lte=5000).order_by('distance')


class LocationSearchView(APIView):
    def get(self, request):
        query = request.GET.get("query","")
        locations = Location.objects.filter(city__icontains=query)[:10]
        data = [{"id": loc.id, "name": f"{loc.city},{loc.area}" }for loc in locations]
        return Response(data)