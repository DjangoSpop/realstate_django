from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django_ratelimit.decorators import ratelimit
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from properties.models import Property
from properties.serializers import PropertySerializer
from .models import CustomUser
from .serializers import UserSerializer, RegisterSerializer

# Registration View
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    @ratelimit(key='ip', rate='5/m')
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "success": True,
            "data": {
                "token": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                "user": UserSerializer(user).data,
            }
        }, status=status.HTTP_201_CREATED)
class PasswordResetView(generics.GenericAPIView):
    def post(self, request):
        email = request.data.get('email')
        user = CustomUser.objects.get(email=email)
        if not user:
            return Response({"success": False, "error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        token = PasswordResetTokenGenerator().make_token(user)
        reset_link = f"http://127.0.0.1:8000/password/reset/{token}"
        send_mail(
            subject="Password Reset",
            message=reset_link,
            recipient_list=[email],
            from_email="admin@realstate.com",
        )
        return Response({"success": True , "message" : "Reset link sent to email"})

class UserFavoritesView(APIView):
    def get(self, request):
        favorites = request.user.favorites.all()
        serializer = PropertySerializer(favorites, many=True)
        return Response({"success": True, "data": serializer.data})

    def post(self, request):
        property_id = request.data.get("property_id")
        property_obj = Property.objects.get(id=property_id)
        request.user.favorites.add(property_obj)
        return Response({"success": True, "message": "Property added to favorites"})

    def delete(self, request, property_id):
        property_obj = Property.objects.get(id=property_id)
        request.user.favorites.remove(property_obj)
        return Response({"success": True, "message": "Property removed from favorites"})


