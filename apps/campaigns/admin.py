from django.contrib import admin
from .models import EmailCampaign

@admin.register(EmailCampaign)
class EmailCampaignAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'status', 'scheduled_time', 'sent_time')
    list_filter = ('status',)
    search_fields = ('user__email', 'name', 'subject')
    raw_id_fields = ('user',)
    date_hierarchy = 'scheduled_time'
    ordering = ('-scheduled_time',)
