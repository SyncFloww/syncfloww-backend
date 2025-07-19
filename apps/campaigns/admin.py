from django.contrib import admin
<<<<<<< HEAD

# Register your models here.
=======
from .models import EmailCampaign

@admin.register(EmailCampaign)
class EmailCampaignAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'status', 'scheduled_time', 'sent_time')
    list_filter = ('status',)
    search_fields = ('user__email', 'name', 'subject')
    raw_id_fields = ('user',)
    date_hierarchy = 'scheduled_time'
    ordering = ('-scheduled_time',)
>>>>>>> f3f460e4d9735213c1a8a8cc1b9cec37ca680d72
