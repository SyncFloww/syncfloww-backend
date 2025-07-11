from django.contrib import admin
from apps.AIs.models import LLMProvider, AIModel, AIAgent, AgentTask

class AIModelInline(admin.TabularInline):
    model = AIModel
    extra = 1

@admin.register(LLMProvider)
class LLMProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'provider_class', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'provider_class')
    inlines = [AIModelInline]

@admin.register(AIModel)
class AIModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'model_id', 'provider', 'model_type', 'is_active')
    list_filter = ('provider', 'model_type', 'is_active')
    search_fields = ('name', 'model_id', 'description')
    list_select_related = ('provider',)

class AgentTaskInline(admin.TabularInline):
    model = AgentTask
    extra = 0
    readonly_fields = ('status', 'created_at', 'updated_at')
    can_delete = False

@admin.register(AIAgent)
class AIAgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'task_type', 'model', 'is_active')
    list_filter = ('task_type', 'is_active')
    search_fields = ('name', 'description')
    list_select_related = ('model', 'model__provider')
    inlines = [AgentTaskInline]
    filter_horizontal = ()

@admin.register(AgentTask)
class AgentTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'agent', 'status', 'created_at')
    list_filter = ('status', 'agent__task_type')
    search_fields = ('agent__name', 'input_data')
    readonly_fields = ('created_at', 'updated_at', 'completed_at')
    list_select_related = ('agent', 'agent__model', 'agent__model__provider')
