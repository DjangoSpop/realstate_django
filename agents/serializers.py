from rest_framework import serializers
from users.models import CustomUser
from properties.models import Property  # Assuming Property is defined elsewhere

class AgentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone', 'company', 'avatar', 'is_public']

class AgentPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'phone', 'company', 'avatar']

class AgentPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['id', 'title', 'price', 'status', 'type', 'views']
