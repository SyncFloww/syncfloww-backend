from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import LLMProvider, AIModel, AIAgent, AgentTask
from .serializers import (
    LLMProviderSerializer,
    AIModelSerializer,
    AIAgentSerializer,
    AgentTaskSerializer
)
from .tasks import execute_agent_task

# ViewSet for managing LLMProvider objects via REST API
class LLMProviderViewSet(viewsets.ModelViewSet):
    # Queryset to retrieve all LLMProvider instances
    queryset = LLMProvider.objects.all()
    # Serializer class to convert model instances to JSON and vice versa
    serializer_class = LLMProviderSerializer
    # Fields that can be used to filter the queryset
    filterset_fields = ['is_active']
    # Fields that can be searched via query parameters
    search_fields = ['name', 'provider_class']

# ViewSet for managing AIModel objects via REST API
class AIModelViewSet(viewsets.ModelViewSet):
    # Queryset with related provider objects for efficient DB access
    queryset = AIModel.objects.select_related('provider')
    serializer_class = AIModelSerializer
    filterset_fields = ['provider', 'model_type', 'is_active']
    search_fields = ['name', 'model_id', 'description']

# ViewSet for managing AIAgent objects via REST API
class AIAgentViewSet(viewsets.ModelViewSet):
    queryset = AIAgent.objects.select_related('model', 'model__provider')
    serializer_class = AIAgentSerializer
    filterset_fields = ['task_type', 'is_active']
    search_fields = ['name', 'description']

    # Custom action to execute an agent task asynchronously
    @action(detail=True, methods=['post'])
    def execute(self, request, pk=None):
        # Retrieve the agent instance by primary key
        agent = self.get_object()
        # Create a new AgentTask with input data from the request
        task = AgentTask.objects.create(
            agent=agent,
            input_data=request.data,
            status='pending'
        )
        # Trigger asynchronous execution of the task
        execute_agent_task.delay(task.id)
        # Return serialized task data with HTTP 201 Created status
        return Response(
            AgentTaskSerializer(task).data,
            status=status.HTTP_201_CREATED
        )

# Read-only ViewSet for AgentTask objects
class AgentTaskViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AgentTaskSerializer
    filterset_fields = ['agent', 'status']
    search_fields = ['agent__name', 'input_data']
    queryset = AgentTask.objects.select_related(
        'agent',
        'agent__model',
        'agent__model__provider'
    ).order_by('-created_at')
