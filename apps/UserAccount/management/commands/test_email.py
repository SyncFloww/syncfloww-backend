from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Send a test email to verify email backend configuration'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email address to send the test email to')

    def handle(self, *args, **options):
        email = options['email']
        subject = 'Test Email from SyncFlow'
        message = 'This is a test email to verify the email backend configuration.'
        from_email = settings.DEFAULT_FROM_EMAIL
        try:
            send_mail(subject, message, from_email, [email])
            self.stdout.write(self.style.SUCCESS(f'Successfully sent test email to {email}'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Failed to send test email: {e}'))
