from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.core.models import Brand
from django.utils import timezone
from .utils import get_auth_provider

SOCIAL_PLATFORM_CHOICES = [
    ('amazon', 'amazon'),
    ('angellist', 'angellist'),
    ('digitalocean', 'digitalocean'),
    ('discord', 'discord'),
    ('dropbox', 'dropbox'),
    ('facebook', 'facebook'),
    ('figma', 'figma'),
    ('frontier', 'frontier'),
    ('fxa', 'fxa'),
    ('gitea', 'gitea'),
    ('github', 'github'),
    ('gitlab', 'gitlab'),
    ('google', 'google'),
    ('gumroad', 'gumroad'),
    ('instagram', 'instagram'),
    ('linkedin', 'linkedin'),
    ('meetup', 'meetup'),
    ('microsoft', 'microsoft'),
    ('notion', 'notion'),
    ('openid_connect', 'openid_connect'),
    ('pinterest', 'pinterest'),
    ('reddit', 'reddit'),
    ('shopify', 'shopify'),
    ('slack', 'slack'),
    ('snapchat', 'snapchat'),
    ('soundcloud', 'soundcloud'),
    ('spotify', 'spotify'),
    ('telegram', 'telegram'),
    ('twitch', 'twitch'),
    ('twitter', 'twitter'),
    ('twitter', 'twitter'),
    ('vimeo', 'vimeo'),
    ('vk', 'vk'),
    ('yahoo', 'yahoo'),
    ('zoom', 'zoom'),
]

class SocialAccount(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='social_accounts'
    )
    brand = models.ForeignKey(
        'core.Brand',
        on_delete=models.CASCADE,
        related_name='social_accounts'
    )
    platform = models.CharField(max_length=20)
    username = models.CharField(max_length=100)
    access_token = models.TextField()
    refresh_token = models.TextField(blank=True, null=True)
    token_expires_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    meta_data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'platform', 'brand')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.platform} ({self.brand.name})"

    @property
    def is_token_valid(self):
        if not self.token_expires_at:
            return True
        return self.token_expires_at > timezone.now()

    def refresh_access_token(self):
        if not self.refresh_token:
            return False
        
        try:
            provider = get_auth_provider(self.platform)
            token_data = provider.refresh_token(self.refresh_token)
            
            self.access_token = token_data['access_token']
            self.refresh_token = token_data.get('refresh_token', self.refresh_token)
            self.token_expires_at = token_data.get('expires_at')
            self.save()
            return True
        except Exception:
            return False

class ScheduledPost(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='scheduled_posts'
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name='scheduled_posts',
        null=True,
        blank=True
    )
    social_accounts = models.ManyToManyField(SocialAccount)
    content = models.TextField()
    media = models.FileField(upload_to='scheduled_posts/', blank=True, null=True)
    scheduled_time = models.DateTimeField()
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-scheduled_time']

    def __str__(self):
        return f"Post by {self.user.email} at {self.scheduled_time}"
