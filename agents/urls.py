from django.urls import path
from .views import AgentListView, AgentProfileView, AgentPropertiesView, AgentStatsView

urlpatterns = [
    path('', AgentListView.as_view(), name='agent-list'),  # GET: List all agents
    path('profile/', AgentProfileView.as_view(), name='agent-profile'),  # GET, PATCH: Manage agent profile
    path('<int:agent_id>/properties/', AgentPropertiesView.as_view(), name='agent-properties'),  # GET: Agent's properties
    path('<int:agent_id>/stats/', AgentStatsView.as_view(), name='agent-stats'),  # GET: Agent statistics
]
