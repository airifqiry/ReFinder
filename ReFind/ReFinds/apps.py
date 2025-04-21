from django.apps import AppConfig

class RefindsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ReFinds'


    def ready(self):
        import ReFinds.signals
