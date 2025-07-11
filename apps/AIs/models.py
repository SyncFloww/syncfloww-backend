from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


# Model representing a Large Language Model (LLM) Provider
class LLMProvider(models.Model):
    # Name of the provider, must be unique
    name = models.CharField(max_length=100, unique=True)
    # Class name or identifier for the provider implementation
    provider_class = models.CharField(max_length=100)
    # Base URL for API requests to the provider
    base_url = models.URLField(blank=True, null=True)
    # API key for authenticating with the provider
    api_key = models.CharField(max_length=255, blank=True, null=True)
    # Flag indicating if the provider is active
    is_active = models.BooleanField(default=True)
    # Timestamp when the provider was created
    created_at = models.DateTimeField(auto_now_add=True)
    # Timestamp when the provider was last updated
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "LLM Provider"
        verbose_name_plural = "LLM Providers"
        ordering = ['name']

    def __str__(self):
        # String representation of the provider
        return self.name

# Model representing an AI Model provided by an LLM Provider
class AIModel(models.Model):
    # Choices for the type of AI model
    MODEL_TYPES = [
        ('text', 'Text Generation'),
        ('image', 'Image Generation'),
        ('multimodal', 'Multimodal'),
        ('embedding', 'Embedding'),
        ('moderation', 'Moderation'),
    ]

    # Name of the AI model
    name = models.CharField(max_length=100)
    # Unique identifier for the model within the provider
    model_id = models.CharField(max_length=100)
    # Foreign key to the LLMProvider that provides this model
    provider = models.ForeignKey(LLMProvider, on_delete=models.CASCADE, related_name='models')
    # Type of the model, chosen from MODEL_TYPES
    model_type = models.CharField(max_length=20, choices=MODEL_TYPES)
    # Optional description of the model
    description = models.TextField(blank=True)
    # Token context window size for the model
    context_window = models.PositiveIntegerField(help_text="Token context window size", null=True, blank=True)
    # Flag indicating if the model is active
    is_active = models.BooleanField(default=True)
    # Timestamp when the model was created
    created_at = models.DateTimeField(auto_now_add=True)
    # Timestamp when the model was last updated
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "AI Model"
        verbose_name_plural = "AI Models"
        unique_together = ('provider', 'model_id')
        ordering = ['provider', 'name']

    def __str__(self):
        # String representation combining provider name and model name
        return f"{self.provider.name}: {self.name}"

# Model representing an AI Agent that performs specific tasks
class AIAgent(models.Model):
    # Choices for the type of task the agent performs
    TASK_TYPES = [
        ('content', 'Content Generation'),
        ('engagement', 'Engagement & Replies'),
        ('moderation', 'Content Moderation'),
        ('analysis', 'Data Analysis'),
        ('scheduling', 'Post Scheduling'),
    ]

    # Name of the AI agent
    name = models.CharField(max_length=100)
    # Description of the agent's purpose or functionality
    description = models.TextField()
    # Task type chosen from TASK_TYPES
    task_type = models.CharField(max_length=20, choices=TASK_TYPES)
    # Foreign key to the AIModel used by this agent
    model = models.ForeignKey(AIModel, on_delete=models.CASCADE, related_name='agents')
    # Configuration data for the agent stored as JSON
    config = models.JSONField(default=dict)
    # Flag indicating if the agent is active
    is_active = models.BooleanField(default=True)
    # Timestamp when the agent was created
    created_at = models.DateTimeField(auto_now_add=True)
    # Timestamp when the agent was last updated
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "AI Agent"
        verbose_name_plural = "AI Agents"
        ordering = ['task_type', 'name']

    def __str__(self):
        # String representation showing task type and agent name
        return f"{self.get_task_type_display()}: {self.name}"

# Model representing a task executed by an AI Agent
class AgentTask(models.Model):
    # Foreign key to the AIAgent that owns this task
    agent = models.ForeignKey(AIAgent, on_delete=models.CASCADE, related_name='tasks')
    # Input data for the task stored as JSON
    input_data = models.JSONField()
    # Output data from the task, optional and stored as JSON
    output_data = models.JSONField(null=True, blank=True)
    # Status of the task with choices for lifecycle stages
    status = models.CharField(max_length=20, default='pending', choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ])
    # Timestamp when the task was created
    created_at = models.DateTimeField(auto_now_add=True)
    # Timestamp when the task was last updated
    updated_at = models.DateTimeField(auto_now=True)
    # Timestamp when the task was completed, optional
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        # String representation showing task ID and agent name
        return f"Task {self.id} for {self.agent.name}"


class AIConfiguration(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ai_configurations'
    )
    name = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    temperature = models.FloatField(default=0.7)
    max_length = models.IntegerField(default=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('AI Configuration')
        verbose_name_plural = _('AI Configurations')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email}'s AI config: {self.name}"
