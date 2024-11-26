from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from agents.serializers import AgentPublicSerializer, AgentProfileSerializer, AgentPropertySerializer
from leads.models import Lead
from properties.models import Property
from users.models import CustomUser


class AgentListView(ListAPIView):
    queryset = CustomUser.filter(role='agent', is_public=True)
    serializer_class = AgentPublicSerializer
# Create your views here.
class AgentProfileView(APIView):
    permissin_classes = [IsAuthenticated]

    def get(self, request):
        serializer = AgentProfileSerializer(request.user)
        return Response({"success": True, "data": serializer.data})

    def patch(self, request):
        serializer = AgentProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data})
        return Response({"success": False, "errors": serializer.errors}, status=400)
class AgentPropertiesView(APIView):
    def get(self, request, agent_id):
        properties = property.objects.filter(agent=agent_id)
        serializer = AgentPropertySerializer(properties, many=True)
        return Response({"sucess":True, "data":serializer.data})
class AgentStatsView(APIView):
    def get(self, request, agent_id):
        total_properties = Property.objects.filter(agent_id=agent_id).count()
        total_leads = Lead.objects.filter(agent_id=agent_id).count()
        sold_properties = Property.objects.filter(agent_id=agent_id, status='sold').count()
        stats = {
            "total_properties": total_properties,
            "total_leads": total_leads,
            "sold_properties": sold_properties,
        }
        return Response({"success": True, "data": stats})
