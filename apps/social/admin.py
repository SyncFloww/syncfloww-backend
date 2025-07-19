from django.contrib import admin
<<<<<<< HEAD

# Register your models here.
=======
from .models import SocialAccount

@admin.register(SocialAccount)
class SocialAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'platform', 'username', 'is_active', 'created_at')
    list_filter = ('platform', 'is_active')
    search_fields = ('user__email', 'username')
    raw_id_fields = ('user',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
>>>>>>> f3f460e4d9735213c1a8a8cc1b9cec37ca680d72
