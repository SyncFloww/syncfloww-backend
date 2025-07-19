from .facebook import FacebookAuthProvider

def get_auth_provider(platform):
    if platform == 'facebook':
        return FacebookAuthProvider()
    # Add other platforms here as elif blocks
    raise ValueError(f"Unsupported platform: {platform}")
