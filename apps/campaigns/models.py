from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

EMAIL_CAMPAIGN_STATUS_CHOICES = [
    ('draft', 'Draft'),
    ('scheduled', 'Scheduled'),
    ('sending', 'Sending'),
    ('sent', 'Sent'),
    ('failed', 'Failed'),
]

class EmailCampaign(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='email_campaigns'
    )
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=255)
    content = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=EMAIL_CAMPAIGN_STATUS_CHOICES,
        default='draft'
    )
    scheduled_time = models.DateTimeField(blank=True, null=True)
    sent_time = models.DateTimeField(blank=True, null=True)
    recipient_list = models.TextField(help_text="Comma-separated list of email addresses")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('email campaign')
        verbose_name_plural = _('email campaigns')
        ordering = ['-scheduled_time']

    def __str__(self):
        return f"{self.user.email}'s campaign: {self.name}"
