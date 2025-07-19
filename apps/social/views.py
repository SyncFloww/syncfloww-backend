<<<<<<< HEAD
from django.shortcuts import render

# Create your views here.
=======
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import redirect
from urllib.parse import urlencode
import json
import uuid
from .auth_providers import get_auth_provider
from .models import SocialAccount
from apps.core.models import Brand
from .serializers import SocialAccountSerializer
from pathlib import Path
import environ

# Load env
env = environ.Env()
environ.Env.read_env(Path(__file__).resolve().parent.parent.parent / '.env')

FRONTEND_URL = env('FRONTEND_URL')

class SocialAuthInitView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, platform):
        try:
            brand_id = request.query_params.get('brand_id')
            redirect_uri = request.query_params.get('redirect_uri')
            
            if not brand_id:
                return Response(
                    {'error': 'brand_id is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                brand = Brand.objects.get(id=brand_id, user=request.user)
            except Brand.DoesNotExist:
                return Response(
                    {'error': 'Brand not found or you do not have permission'},
                    status=status.HTTP_404_NOT_FOUND
                )

            provider = get_auth_provider(platform)
            
            # Generate state with platform and brand info
            state = {
                'platform': platform,
                'brand_id': brand_id,
                'nonce': str(uuid.uuid4()),
                'redirect_uri': redirect_uri
            }
            encoded_state = json.dumps(state)
            
            auth_url = provider.get_auth_url(
                state=encoded_state,
                redirect_uri=redirect_uri
            )
            
            return Response({'auth_url': auth_url})
            
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': 'Failed to initialize authentication'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class SocialAuthCallbackView(APIView):
    def get(self, request):
        try:
            code = request.GET.get('code')
            state = json.loads(request.GET.get('state'))
            
            if not code or not state:
                return Response(
                    {'error': 'Missing code or state'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            platform = state['platform']
            brand_id = state['brand_id']
            redirect_uri = state.get('redirect_uri')
            
            provider = get_auth_provider(platform)
            
            # Exchange code for tokens
            token_data = provider.exchange_code_for_token(
                code=code,
                redirect_uri=redirect_uri
            )
            
            # Get long-lived token if available
            if hasattr(provider, 'get_long_lived_token'):
                token_data = provider.get_long_lived_token(token_data['access_token'])
            
            # Get user info
            user_info = provider.get_user_info(token_data['access_token'])
            
            # Get or create social account
            brand = Brand.objects.get(id=brand_id)
            account, created = SocialAccount.objects.update_or_create(
                user=request.user,
                brand=brand,
                platform=platform,
                defaults={
                    'username': user_info.get('name', ''),
                    'access_token': token_data['access_token'],
                    'refresh_token': token_data.get('refresh_token', ''),
                    'token_expires_at': token_data.get('expires_at'),
                    'meta_data': {
                        'user_info': user_info,
                        'scopes': token_data.get('scope', '').split(',')
                    },
                    'is_active': True
                }
            )
            
            # Redirect back to frontend with success status
            frontend_redirect = f"{FRONTEND_URL}/social/connected?status=success&account_id={account.id}"
            return redirect(frontend_redirect)
            
        except Exception as e:
            # Redirect back to frontend with error status
            frontend_redirect = f"{FRONTEND_URL}/social/connected?status=error&message={str(e)}"
            return redirect(frontend_redirect)


class SocialAccountListCreateView(generics.ListCreateAPIView):
    queryset = SocialAccount.objects.all()
    serializer_class = SocialAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SocialAccountRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SocialAccount.objects.all()
    serializer_class = SocialAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
>>>>>>> f3f460e4d9735213c1a8a8cc1b9cec37ca680d72
