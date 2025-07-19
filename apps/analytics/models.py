from django.db import models
<<<<<<< HEAD

# Create your models here.
=======
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.social.models import SocialAccount

class AnalyticsData(models.Model):
    social_account = models.ForeignKey(
        SocialAccount,
        on_delete=models.CASCADE,
        related_name='analytics_data'
    )
    date = models.DateField()
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    impressions = models.IntegerField(default=0)
    reach = models.IntegerField(default=0)
    profile_views = models.IntegerField(default=0)
    website_clicks = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('analytics data')
        verbose_name_plural = _('analytics data')
        unique_together = ('social_account', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.social_account.platform} analytics for {self.date}"
>>>>>>> f3f460e4d9735213c1a8a8cc1b9cec37ca680d72
