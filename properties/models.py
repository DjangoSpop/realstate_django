from django.db import models
from users.models import CustomUser

class Location(models.Model):

    address = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    coordinates = models.JSONField(blank=True, null=True)   # {"lat": float, "lng": float}

    def __str__(self):
        return f"{self.city}, {self.address}"
class Property(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('apartment', 'Apartment'),
        ('villa', 'Villa'),
        ('duplex', 'Duplex'),
        ('penthouse', 'Penthouse'),
        ('building', 'Building'),
    ]
    LISTING_TYPE_CHOICES = [
        ('sale', 'Sale'),
        ('rent', 'Rent'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('rented', 'Rented'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="properties")
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    area = models.FloatField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField() # JSON for city, address, and coordinates
    features = models.JSONField(blank=True, null=True)  # List of features
    images = models.JSONField()  # [{"id": ..., "url": ..., "main": ...}]
    amenities = models.JSONField(blank=True, null=True)  # List of amenities
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    agent = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='listed_properties')
    views = models.IntegerField(default=0)
    favorites = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PropertyImage(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='property_images',  # Adjusted related_name
    )
    image = models.ImageField(upload_to='property_images/')
    is_main = models.BooleanField(default=False)
    ordering = models.IntegerField(default=0)

    class Meta:
        ordering = ['ordering']

    def __str__(self):
        return f"Image for {self.property.title}"



