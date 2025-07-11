from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.social.models import SocialAccount

CONTENT_STATUS_CHOICES = [
    ('draft', 'Draft'),
    ('scheduled', 'Scheduled'),
    ('published', 'Published'),
    ('failed', 'Failed'),
]

CONTENT_TYPE_CHOICES = [
    ('post', 'Post'),
    ('story', 'Story'),
    ('reel', 'Reel'),
    ('video', 'Video'),
]

class Content(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='contents'
    )
    social_accounts = models.ManyToManyField(
        SocialAccount,
        related_name='contents'
    )
    title = models.CharField(max_length=255, blank=True)
    text = models.TextField()
    media = models.FileField(upload_to='content/media/', blank=True, null=True)
    content_type = models.CharField(
        max_length=20,
        choices=CONTENT_TYPE_CHOICES,
        default='post'
    )
    status = models.CharField(
        max_length=20,
        choices=CONTENT_STATUS_CHOICES,
        default='draft'
    )
    scheduled_time = models.DateTimeField(blank=True, null=True)
    published_time = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('content')
        verbose_name_plural = _('contents')
        ordering = ['-scheduled_time']

    def __str__(self):
        return f"{self.user.email}'s {self.content_type} - {self.status}"
