from django.contrib import admin
from .models import SocialAccount

@admin.register(SocialAccount)
class SocialAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'platform', 'username', 'is_active', 'created_at')
    list_filter = ('platform', 'is_active')
    search_fields = ('user__email', 'username')
    raw_id_fields = ('user',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
