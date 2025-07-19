from django.db import models
<<<<<<< HEAD

# Create your models here.
=======
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.social.models import SocialAccount

AUTOMATION_TYPE_CHOICES = [
    ('follow', 'Follow'),
    ('unfollow', 'Unfollow'),
    ('like', 'Like'),
    ('comment', 'Comment'),
    ('message', 'Message'),
]

AUTOMATION_STATUS_CHOICES = [
    ('active', 'Active'),
    ('paused', 'Paused'),
    ('completed', 'Completed'),
]

class LLMProvider(models.Model):
    name = models.CharField(max_length=100)
    provider_class = models.CharField(max_length=255)
    api_key_env = models.CharField(max_length=100, blank=True)
    base_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class AIModel(models.Model):
    name = models.CharField(max_length=100)
    model_id = models.CharField(max_length=255)
    provider = models.ForeignKey(LLMProvider, on_delete=models.CASCADE, related_name='models')
    model_type = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class AIAgent(models.Model):
    name = models.CharField(max_length=100)
    task_type = models.CharField(max_length=100)
    model = models.ForeignKey(AIModel, on_delete=models.CASCADE, related_name='agents')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class AgentTask(models.Model):
    agent = models.ForeignKey(AIAgent, on_delete=models.CASCADE, related_name='tasks')
    input_data = models.JSONField(blank=True, null=True)
    status = models.CharField(max_length=50, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Task {self.id} for {self.agent.name}"

class AutomationRule(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='automation_rules'
    )
    social_account = models.ForeignKey(
        SocialAccount,
        on_delete=models.CASCADE,
        related_name='automation_rules'
    )
    name = models.CharField(max_length=100)
    automation_type = models.CharField(
        max_length=20,
        choices=AUTOMATION_TYPE_CHOICES
    )
    status = models.CharField(
        max_length=20,
        choices=AUTOMATION_STATUS_CHOICES,
        default='active'
    )
    target = models.CharField(max_length=100, blank=True)
    message = models.TextField(blank=True)
    daily_limit = models.PositiveIntegerField(default=10)
    interval_minutes = models.PositiveIntegerField(default=30)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('automation rule')
        verbose_name_plural = _('automation rules')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email}'s {self.automation_type} rule"
>>>>>>> f3f460e4d9735213c1a8a8cc1b9cec37ca680d72
