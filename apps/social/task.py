from celery import shared_task
from django.utils import timezone
from .models import SocialAccount
from .auth_providers import get_auth_provider

@shared_task
def refresh_expired_tokens():
    """Refresh access tokens that are about to expire"""
    accounts = SocialAccount.objects.filter(
        token_expires_at__lt=timezone.now() + timezone.timedelta(hours=1),
        is_active=True
    )
    
    for account in accounts:
        account.refresh_access_token()

@shared_task
def post_to_social_media(account_id, content, media_url=None):
    """Post content to a social media account"""
    try:
        account = SocialAccount.objects.get(id=account_id, is_active=True)
        provider = get_auth_provider(account.platform)
        
        # Post to the platform
        result = provider.create_post(
            access_token=account.access_token,
            content=content,
            media_url=media_url
        )
        
        return {
            'status': 'success',
            'result': result
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }
