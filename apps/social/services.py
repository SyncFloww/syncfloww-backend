from django.conf import settings
import requests
from urllib.parse import urlencode

class SocialMediaService:
    @staticmethod
    def get_auth_url(platform: str, callback_url: str) -> str:
        base_urls = {
            'facebook': 'https://www.facebook.com/v12.0/dialog/oauth',
            'twitter': 'https://twitter.com/i/oauth2/authorize',
            'instagram': 'https://api.instagram.com/oauth/authorize',
            'linkedin': 'https://www.linkedin.com/oauth/v2/authorization',
            'pinterest': 'https://www.pinterest.com/oauth',
        }
        
        params = {
            'facebook': {
                'client_id': settings.SOCIAL_AUTH_FACEBOOK_KEY,
                'redirect_uri': callback_url,
                'state': '{st=state123abc,ds=123456789}',
                'scope': 'pages_manage_posts,pages_read_engagement'
            },
            # Add other platforms similarly
        }
        
        return f"{base_urls[platform]}?{urlencode(params[platform])}"

    @staticmethod
    def post_to_social(platform: str, account_id: str, content: str, media_url: str = None) -> bool:
        # Implementation would use each platform's API
        # This is a simplified version
        try:
            # In real implementation, we'd use the platform's SDK or API
            print(f"Posted to {platform} account {account_id}: {content}")
            if media_url:
                print(f"With media: {media_url}")
            return True
        except Exception as e:
            print(f"Error posting to {platform}: {str(e)}")
            return False
