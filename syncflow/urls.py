from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage



urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication and user management
    path('api/accounts/', include('apps.UserAccount.urls', namespace='accounts')),
    
    # Social media features
    path('api/social/', include('apps.social.urls')),
    
    # Analytics
    path('api/analytics/', include('apps.analytics.urls')),
    
    # Automations
    path('api/automations/', include('apps.automations.urls')),
    
    # Campaigns
    path('api/campaigns/', include('apps.campaigns.urls')),
    
    # Integrations
    path('api/integrations/', include('apps.integrations.urls')),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    #Favicon path
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'))),
]


# static files (when using runserver with --insecure)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    if hasattr(settings, 'STATICFILES_DIRS') and settings.STATICFILES_DIRS:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
