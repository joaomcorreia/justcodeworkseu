"""
Simple Translation Management System for JustCodeWorks
Provides basic translation functionality without requiring gettext tools
"""

from django.db import models
from django.contrib.auth.models import User


class TranslationKey(models.Model):
    """
    Translation key model for storing translatable strings
    """
    key = models.CharField(max_length=255, unique=True, help_text="Translation key (e.g., 'admin.dashboard.title')")
    description = models.TextField(blank=True, help_text="Description of what this key is used for")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['key']

    def __str__(self):
        return self.key

    def get_completion_percentage(self):
        """Calculate completion percentage for this key"""
        total_languages = Translation.objects.filter(key=self).values('language').distinct().count()
        expected_languages = 6  # en, nl, de, fr, es, pt
        return int((total_languages / expected_languages) * 100) if expected_languages > 0 else 0


class Translation(models.Model):
    """
    Translation model for storing actual translations
    """
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('nl', 'Nederlands'),
        ('de', 'Deutsch'),
        ('fr', 'Français'),
        ('es', 'Español'),
        ('pt', 'Português'),
    ]

    key = models.ForeignKey(TranslationKey, on_delete=models.CASCADE, related_name='translations')
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES)
    value = models.TextField(help_text="The translated text")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ['key', 'language']
        ordering = ['language', 'key__key']

    def __str__(self):
        return f"{self.key.key} ({self.language}): {self.value[:50]}..."


class LanguageSettings(models.Model):
    """
    Language configuration settings
    """
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('nl', 'Nederlands'),
        ('de', 'Deutsch'),
        ('fr', 'Français'),
        ('es', 'Español'),
        ('pt', 'Português'),
    ]

    default_language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default='en')
    fallback_language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default='en')
    active_languages = models.JSONField(default=list, help_text="List of active language codes")
    auto_translate = models.BooleanField(default=False, help_text="Enable automatic translation using AI")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Language Settings"
        verbose_name_plural = "Language Settings"

    def __str__(self):
        return f"Language Settings (Default: {self.default_language})"

    @classmethod
    def get_settings(cls):
        """Get or create language settings"""
        settings, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                'default_language': 'en',
                'fallback_language': 'en',
                'active_languages': ['en', 'nl', 'de', 'fr', 'es', 'pt']
            }
        )
        return settings


def get_translation(key, language='en', fallback=''):
    """
    Get a translation for a given key and language
    """
    try:
        translation = Translation.objects.get(key__key=key, language=language, is_active=True)
        return translation.value
    except Translation.DoesNotExist:
        # Try fallback language
        try:
            settings = LanguageSettings.get_settings()
            if language != settings.fallback_language:
                translation = Translation.objects.get(
                    key__key=key, 
                    language=settings.fallback_language, 
                    is_active=True
                )
                return translation.value
        except Translation.DoesNotExist:
            pass
        
        # Return fallback or key if no translation found
        return fallback or key


def create_translation_key(key, description='', translations=None):
    """
    Create a new translation key with optional translations
    """
    translation_key, created = TranslationKey.objects.get_or_create(
        key=key,
        defaults={'description': description}
    )
    
    if translations and isinstance(translations, dict):
        for lang_code, value in translations.items():
            if lang_code in [choice[0] for choice in Translation.LANGUAGE_CHOICES]:
                Translation.objects.update_or_create(
                    key=translation_key,
                    language=lang_code,
                    defaults={
                        'value': value,
                        'is_active': True
                    }
                )
    
    return translation_key


def get_translation_statistics():
    """
    Get translation completion statistics for all languages
    """
    stats = []
    total_keys = TranslationKey.objects.count()
    
    for lang_code, lang_name in Translation.LANGUAGE_CHOICES:
        translated_keys = Translation.objects.filter(
            language=lang_code, 
            is_active=True
        ).count()
        
        completion = int((translated_keys / total_keys) * 100) if total_keys > 0 else 0
        
        stats.append({
            'code': lang_code,
            'name': lang_name,
            'completion': completion,
            'translated': translated_keys,
            'total': total_keys
        })
    
    return stats


def initialize_default_translations():
    """
    Initialize default translation keys for the admin interface
    """
    default_translations = {
        'admin.dashboard.title': {
            'description': 'Dashboard page title',
            'translations': {
                'en': 'Dashboard Overview',
                'nl': 'Dashboard Overzicht',
                'de': 'Dashboard Übersicht',
                'fr': 'Aperçu du tableau de bord',
                'es': 'Vista general del panel',
                'pt': 'Visão geral do painel'
            }
        },
        'admin.website.title': {
            'description': 'Website management page title',
            'translations': {
                'en': 'Website Management',
                'nl': 'Website Beheer',
                'de': 'Website Verwaltung',
                'fr': 'Gestion du site web',
                'es': 'Gestión del sitio web',
                'pt': 'Gestão do website'
            }
        },
        'admin.analytics.title': {
            'description': 'Analytics dashboard title',
            'translations': {
                'en': 'Analytics Dashboard',
                'nl': 'Analytics Dashboard',
                'de': 'Analytics Dashboard',
                'fr': 'Tableau de bord analytique',
                'es': 'Panel de análisis',
                'pt': 'Painel de análises'
            }
        },
        'admin.settings.title': {
            'description': 'Settings page title',
            'translations': {
                'en': 'Site Settings',
                'nl': 'Website Instellingen',
                'de': 'Website Einstellungen',
                'fr': 'Paramètres du site',
                'es': 'Configuración del sitio',
                'pt': 'Configurações do site'
            }
        },
        'admin.translations.title': {
            'description': 'Translation management page title',
            'translations': {
                'en': 'Translation Management',
                'nl': 'Vertalingen Beheer',
                'de': 'Übersetzungsverwaltung',
                'fr': 'Gestion des traductions',
                'es': 'Gestión de traducciones',
                'pt': 'Gestão de traduções'
            }
        }
    }
    
    for key, data in default_translations.items():
        create_translation_key(
            key=key,
            description=data['description'],
            translations=data['translations']
        )