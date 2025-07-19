from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Brand(models.Model):
    class Meta:
        app_label = 'core'
        ordering = ['-created_at']
        unique_together = ('user', 'name')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='brands'
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='brands/logos/', blank=True, null=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (Owner: {self.user.email})"
