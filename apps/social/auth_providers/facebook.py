import requests
from django.conf import settings
from urllib.parse import urlencode

class FacebookAuthProvider:
    def __init__(self):
        self.config = settings.SOCIAL_AUTH_CONFIGS['facebook']
        
    def get_auth_url(self, state, redirect_uri=None):
        params = {
            'client_id': self.config['CLIENT_ID'],
            'redirect_uri': redirect_uri or self.config['REDIRECT_URI'],
            'state': state,
            'response_type': 'code',
            'scope': ','.join(self.config['SCOPE']),
            'auth_type': 'rerequest',
            'display': 'popup'
        }
        return f"{self.config['AUTH_URL']}?{urlencode(params)}"
    
    def exchange_code_for_token(self, code, redirect_uri=None):
        data = {
            'client_id': self.config['CLIENT_ID'],
            'client_secret': self.config['CLIENT_SECRET'],
            'redirect_uri': redirect_uri or self.config['REDIRECT_URI'],
            'code': code,
            'grant_type': 'authorization_code'
        }
        
        response = requests.post(
            self.config['TOKEN_URL'],
            data=data,
            headers={'Accept': 'application/json'}
        )
        response.raise_for_status()
        return response.json()
    
    def get_user_info(self, access_token):
        fields = ['id', 'name', 'email', 'picture']
        response = requests.get(
            f"https://graph.facebook.com/v12.0/me",
            params={
                'access_token': access_token,
                'fields': ','.join(fields)
            }
        )
        response.raise_for_status()
        return response.json()
    
    def get_long_lived_token(self, short_lived_token):
        response = requests.get(
            f"https://graph.facebook.com/v12.0/oauth/access_token",
            params={
                'grant_type': 'fb_exchange_token',
                'client_id': self.config['CLIENT_ID'],
                'client_secret': self.config['CLIENT_SECRET'],
                'fb_exchange_token': short_lived_token
            }
        )
        response.raise_for_status()
        return response.json()

    def create_post(self, access_token, content, media_url=None):
        """Create a post on the user's Facebook timeline or page."""
        post_url = f"https://graph.facebook.com/v12.0/me/feed"
        data = {
            'message': content,
            'access_token': access_token
        }
        if media_url:
            data['link'] = media_url
        
        response = requests.post(post_url, data=data)
        response.raise_for_status()
        return response.json()
