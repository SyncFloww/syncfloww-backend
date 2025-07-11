from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse
from django.http import HttpResponseRedirect

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        url = reverse('accounts:account_confirm_email', args=[emailconfirmation.key])
        return request.build_absolute_uri(url)

    def respond_email_verification_sent(self, request, user):
        url = reverse('accounts:account_email_verification_sent')
        return HttpResponseRedirect(url)
