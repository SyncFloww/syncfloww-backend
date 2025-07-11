from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from dj_rest_auth.views import (
    LoginView, LogoutView, PasswordResetView,
    PasswordChangeView,
)
from dj_rest_auth.registration.views import RegisterView, VerifyEmailView
from .views import (
    UserProfileView,
    current_user,
    CustomPasswordResetConfirmView,
    CustomRegisterView,
    CustomVerifyEmailView,
    AccountEmailVerificationSentView,
)

router = DefaultRouter()

app_name='accounts'

urlpatterns = [
    # Authentication URLs
    path('auth/register/', CustomRegisterView.as_view(), name='rest_register'),
    path('auth/login/', LoginView.as_view(), name='rest_login'),
    path('auth/logout/', LogoutView.as_view(), name='rest_logout'),
    path('auth/user/', current_user, name='rest_user_details'),
    path('auth/password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    path('auth/password/reset/confirm/<uidb64>/<token>/', 
         CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('auth/password/change/', PasswordChangeView.as_view(), name='rest_password_change'),
    
    # Email verification URLs
    path('auth/verify-email/', CustomVerifyEmailView.as_view(), name='rest_verify_email'),
    path('account-confirm-email/<str:key>/', CustomVerifyEmailView.as_view(), 
         name='account_confirm_email'),
    path('account-email-verification-sent/', AccountEmailVerificationSentView.as_view(), name='account_email_verification_sent'),
    
    # Profile URLs
    path('profile/', UserProfileView.as_view(), name='user_profile'),
]
