from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import serializers
from dj_rest_auth.views import PasswordResetConfirmView
from dj_rest_auth.registration.views import RegisterView, VerifyEmailView
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from .models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer, CustomRegisterSerializer
from django.conf import settings
from rest_framework.views import APIView
from allauth.account.models import EmailConfirmationHMAC
from django.http import HttpResponseBadRequest
from rest_framework_simplejwt.tokens import RefreshToken
from django.views import View

<<<<<<< HEAD

=======
>>>>>>> f3f460e4d9735213c1a8a8cc1b9cec37ca680d72
User = get_user_model()

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Safely get profile or raise 404
        user = self.request.user
        # Use getattr with default None to avoid Pylance warning
        profile = getattr(user, 'profile', None)
        if profile is not None:
            return profile
        else:
            from django.http import Http404
            raise Http404("User profile not found")


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    def get_redirect_url(self):
        return self.request.build_absolute_uri(f"{self.request.scheme}://{self.request.get_host()}/password-reset/confirm/")


class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({"detail": "Registration successful. Please verify your email."}, status=status.HTTP_200_OK, headers=headers)
        except serializers.ValidationError as ve:
            return Response({"errors": ve.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Registration error: {str(e)}", exc_info=True)
            # Handle duplicate email error gracefully
            if 'UNIQUE constraint failed' in str(e):
                return Response({"error": "A user with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"error": "Registration failed."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

<<<<<<< HEAD
class CustomVerifyEmailView(VerifyEmailView):
    def get(self, request, *args, **kwargs): # type: ignore[override]
        key = kwargs.get('key')
        if not key:
            return HttpResponseBadRequest("Missing confirmation key.")
        try:
            confirmation = EmailConfirmationHMAC.from_key(key)
            if not confirmation:
                return HttpResponseBadRequest("Invalid confirmation key.")
            confirmation.confirm(request)
            user = confirmation.email_address.user
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            response = redirect('/api/accounts/auth/user/')
            # Set tokens in cookies
            response.set_cookie('syncflow-auth', str(refresh.access_token), httponly=False)
            response.set_cookie('syncflow-refresh-token', str(refresh), httponly=False)
            return response
        except Exception as e:
            return HttpResponseBadRequest(f"Email confirmation failed: {str(e)}")
=======
# class CustomVerifyEmailView(VerifyEmailView):
#     def get(self, request, *args, **kwargs): # type: ignore[override]
#         key = kwargs.get('key')
#         if not key:
#             return HttpResponseBadRequest("Missing confirmation key.")
#         try:
#             confirmation = EmailConfirmationHMAC.from_key(key)
#             if not confirmation:
#                 return HttpResponseBadRequest("Invalid confirmation key.")
#             confirmation.confirm(request)
#             user = confirmation.email_address.user
#             # Generate JWT tokens
#             refresh = RefreshToken.for_user(user)
#             return render(request, 'account/email_verified.html', {'user':request.user})
#             # response = redirect('/api/accounts/auth/user/')
#             # Set tokens in cookies
#             response.set_cookie('syncflow-auth', str(refresh.access_token), httponly=False)
#             response.set_cookie('syncflow-refresh-token', str(refresh), httponly=False)
#             return response
#         except Exception as e:
#             return HttpResponseBadRequest(f"Email confirmation failed: {str(e)}")
#             return render(request, 'account/email_verification_failed.html')


class CustomVerifyEmailView(VerifyEmailView):
    def get(self, request, *args, **kwargs):  # type: ignore[override]
        key = kwargs.get('key')
        if not key:
            return render(request, 'account/email_verification_failed.html', {
                'message': "Missing confirmation key."
            })

        try:
            confirmation = EmailConfirmationHMAC.from_key(key)
            if not confirmation:
                return render(request, 'account/email_verification_failed.html', {
                    'message': "Invalid or expired confirmation key."
                })

            confirmation.confirm(request)
            user = confirmation.email_address.user

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Render success page
            response = render(request, 'account/email_verified.html', {
                'message': "Your email has been successfully verified.",
                'user': user,
            })

            # Set tokens in cookies
            response.set_cookie('syncflow-auth', access_token, httponly=False)
            response.set_cookie('syncflow-refresh-token', str(refresh), httponly=False)

            return response

        except Exception as e:
            return render(request, 'account/email_verification_failed.html', {
                'message': f"Email verification failed: {str(e)}"
            })
>>>>>>> f3f460e4d9735213c1a8a8cc1b9cec37ca680d72


class AccountEmailVerificationSentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html' or request.META.get('HTTP_ACCEPT', '').startswith('text/html'):
            return render(request, 'account/email_verification_sent.html')
        return Response({"detail": "Email verification sent."}, status=status.HTTP_200_OK)


# class AccountEmailVerificationSentView(APIView):
#     permission_classes = []

#     def get(self, request, *args, **kwargs):
#         message = request.GET.get("message", "Email verification sent successfully.")
#         error = request.GET.get("error", None)

#         context = {
#             "message": message,
#             "error": error
#         }

#         return render(request, 'account/email_verification_sent.html', context)
