from django.contrib import admin
<<<<<<< HEAD

# Register your models here.
=======
from .models import AnalyticsData

@admin.register(AnalyticsData)
class AnalyticsDataAdmin(admin.ModelAdmin):
    list_display = ('social_account', 'date', 'followers', 'likes', 'comments', 'shares')
    list_filter = ('social_account__platform',)
    search_fields = ('social_account__user__email', 'social_account__platform')
    raw_id_fields = ('social_account',)
    date_hierarchy = 'date'
    ordering = ('-date',)
>>>>>>> f3f460e4d9735213c1a8a8cc1b9cec37ca680d72
