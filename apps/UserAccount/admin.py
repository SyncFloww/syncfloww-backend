from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from allauth.account.models import EmailAddress
from django.contrib.admin import ModelAdmin
from .models import User, UserProfile

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ['email', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    ordering = ['email']
    search_fields = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

# Unregister Group if registered
try:
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass

# Unregister EmailAddress to avoid separate admin section
try:
    admin.site.unregister(EmailAddress)
except admin.sites.NotRegistered:
    pass

# Custom admin for EmailAddress to show under accounts app label
class EmailAddressAdmin(ModelAdmin):
    def get_app_label(self, request):
        return "accounts"

# Register User, UserProfile, and EmailAddress under accounts app
try:
    admin.site.register(User, UserAdmin)
except admin.sites.AlreadyRegistered:
    pass

try:
    admin.site.register(UserProfile)
except admin.sites.AlreadyRegistered:
    pass

try:
    admin.site.register(EmailAddress, EmailAddressAdmin)
except admin.sites.AlreadyRegistered:
    pass
