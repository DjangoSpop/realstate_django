from django.db import models
from properties.models import Property
from users.models import CustomUser


class Lead(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('contacted', 'Contacted'),
        ('closed', 'Closed'),
    ]
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='leads')
    name = models.CharField(max_length=255)
    agent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='leads')
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    preferred_time = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Lead for {self.property.title} by {self.name}"
