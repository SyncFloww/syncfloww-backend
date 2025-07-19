from django.apps import AppConfig


class AutomationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.automations'
<<<<<<< HEAD
=======
    
    def ready(self):
        import apps.automations.signals
>>>>>>> f3f460e4d9735213c1a8a8cc1b9cec37ca680d72
