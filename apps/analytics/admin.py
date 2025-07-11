from django.contrib import admin
from .models import AnalyticsData

@admin.register(AnalyticsData)
class AnalyticsDataAdmin(admin.ModelAdmin):
    list_display = ('social_account', 'date', 'followers', 'likes', 'comments', 'shares')
    list_filter = ('social_account__platform',)
    search_fields = ('social_account__user__email', 'social_account__platform')
    raw_id_fields = ('social_account',)
    date_hierarchy = 'date'
    ordering = ('-date',)
