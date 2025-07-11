from django.contrib import admin
from .models import Content

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_type', 'status', 'scheduled_time', 'published_time')
    list_filter = ('content_type', 'status')
    search_fields = ('user__email', 'title', 'text')
    raw_id_fields = ('user', 'social_accounts')
    date_hierarchy = 'scheduled_time'
    ordering = ('-scheduled_time',)
