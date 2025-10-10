from django.apps import AppConfig


class TranslationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'translations'
    verbose_name = 'JustCodeWorks Translations'

    def ready(self):
        """
        Initialize default translations when the app is ready
        """
        try:
            from .models import initialize_default_translations
            # Only initialize in production/when ready
            # initialize_default_translations()
        except Exception:
            # Ignore during migrations
            pass