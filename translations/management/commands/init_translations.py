from django.core.management.base import BaseCommand
from translations.models import initialize_default_translations


class Command(BaseCommand):
    help = 'Initialize default translation keys for JustCodeWorks'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Initializing default translations...')
        )
        
        try:
            initialize_default_translations()
            self.stdout.write(
                self.style.SUCCESS('Default translations initialized successfully!')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error initializing translations: {e}')
            )