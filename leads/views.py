from django_ratelimit.decorators import ratelimit
from rest_framework.response import Response
from rest_framework.views import APIView

class CreateLeadView(APIView):
    @ratelimit(key='ip', rate='3/m')  # Limit to 3 submissions per minute per IP
    def post(self, request, *args, **kwargs):
        # Your lead generation logic here
        return Response({"message": "Lead submission with rate limiting"})
