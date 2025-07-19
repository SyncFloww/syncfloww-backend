from pathlib import Path
import environ

# Load env
env = environ.Env()
environ.Env.read_env(Path(__file__).resolve().parent.parent.parent / '.env')

SOCIAL_AUTH_CONFIGS = {
    'facebook': {
        'CLIENT_ID': env('FACEBOOK_APP_ID'),
        'CLIENT_SECRET': env('FACEBOOK_APP_SECRET'),
        'AUTH_URL': 'https://www.facebook.com/v12.0/dialog/oauth',
        'TOKEN_URL': 'https://graph.facebook.com/v12.0/oauth/access_token',
        'REDIRECT_URI': f"{env('FRONTEND_URL')}/auth/facebook/callback",
        'SCOPE': 'email,public_profile,pages_manage_posts,pages_read_engagement'
    },
    # 'twitter': {
    #     'CLIENT_ID': env('TWITTER_CLIENT_ID'),
    #     'CLIENT_SECRET': env('TWITTER_CLIENT_SECRET'),
    #     'AUTH_URL': 'https://twitter.com/i/oauth2/authorize',
    #     'TOKEN_URL': 'https://api.twitter.com/2/oauth2/token',
    #     'REDIRECT_URI': f"{env('FRONTEND_URL')}/auth/twitter/callback",
    #     'SCOPE': 'tweet.read tweet.write users.read offline.access'
    # },
    # 'instagram': {
    #     'CLIENT_ID': env('INSTAGRAM_CLIENT_ID'),
    #     'CLIENT_SECRET': env('INSTAGRAM_CLIENT_SECRET'),
    #     'AUTH_URL': 'https://api.instagram.com/oauth/authorize',
    #     'TOKEN_URL': 'https://api.instagram.com/oauth/access_token',
    #     'REDIRECT_URI': f"{env('FRONTEND_URL')}/auth/instagram/callback",
    #     'SCOPE': 'user_profile,user_media'
    # },
    # 'linkedin': {
    #     'CLIENT_ID': env('LINKEDIN_CLIENT_ID'),
    #     'CLIENT_SECRET': env('LINKEDIN_CLIENT_SECRET'),
    #     'AUTH_URL': 'https://www.linkedin.com/oauth/v2/authorization',
    #     'TOKEN_URL': 'https://www.linkedin.com/oauth/v2/accessToken',
    #     'REDIRECT_URI': f"{env('FRONTEND_URL')}/auth/linkedin/callback'",
    #     'SCOPE': 'r_liteprofile r_emailaddress w_member_social'
    # },
    # Add configurations for other platforms similarly
}
