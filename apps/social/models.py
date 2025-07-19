from django.conf import settings
from django.db import models
from django.utils import timezone

class SocialPlatform(models.Model):
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
        ('linkedin', 'LinkedIn'),
        ('pinterest', 'Pinterest'),
        ('youtube', 'YouTube'),
        ('tiktok', 'TikTok'),
    ]
    
    name = models.CharField(max_length=20, choices=PLATFORM_CHOICES, unique=True)
    icon = models.CharField(max_length=50, blank=True)
    api_version = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return self.get_name_display()

class SocialAccount(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='social_accounts',
        on_delete=models.CASCADE
    )
    platform = models.ForeignKey(
        SocialPlatform,
        related_name='accounts',
        on_delete=models.CASCADE
    )
    account_name = models.CharField(max_length=255)
    account_id = models.CharField(max_length=255)
    access_token = models.TextField()
    refresh_token = models.TextField(blank=True, null=True)
    token_expires = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'platform', 'account_id')
    
    def __str__(self):
        return f"{self.user.email}'s {self.platform.name} account"

class ScheduledPost(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='scheduled_posts',
        on_delete=models.CASCADE
    )
    account = models.ForeignKey(
        SocialAccount,
        related_name='scheduled_posts',
        on_delete=models.CASCADE
    )
    content = models.TextField()
    media_url = models.URLField(blank=True, null=True)
    scheduled_time = models.DateTimeField()
    is_published = models.BooleanField(default=False)
    published_time = models.DateTimeField(null=True, blank=True)
    post_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Post for {self.account} scheduled for {self.scheduled_time}"
    
    def save(self, *args, **kwargs):
        # Check if the post is being published
        if self.is_published and not self.published_time:
            self.published_time = timezone.now()
        super().save(*args, **kwargs)

class PostAnalytics(models.Model):
    post = models.OneToOneField(
        ScheduledPost,
        related_name='analytics',
        on_delete=models.CASCADE
    )
    likes = models.PositiveIntegerField(default=0)
    comments = models.PositiveIntegerField(default=0)
    shares = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    impressions = models.PositiveIntegerField(default=0)
    engagement_rate = models.FloatField(default=0.0)
    saved_at = models.DateTimeField(auto_now_add=True)
    
    def update_engagement_rate(self):
        if self.impressions > 0:
            self.engagement_rate = (
                (self.likes + self.comments + self.shares + self.clicks) / 
                self.impressions
            )
    
    def save(self, *args, **kwargs):
        self.update_engagement_rate()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Analytics for post {self.post.id}"
