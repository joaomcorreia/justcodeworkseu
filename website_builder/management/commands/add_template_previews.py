"""
Management command to add template screenshots and preview images
"""
import os
from django.core.management.base import BaseCommand
from website_builder.models import WebsiteTemplate


class Command(BaseCommand):
    help = 'Add template screenshots and preview images'

    def handle(self, *args, **options):
        """Add preview images to existing templates"""
        
        # Template preview URLs (using placeholder service for demo)
        template_previews = {
            'professional_template_1': {
                'preview_image': 'https://via.placeholder.com/800x600/007bff/ffffff?text=Professional+Business+Template',
                'thumbnail_image': 'https://via.placeholder.com/300x200/007bff/ffffff?text=Professional',
                'demo_url': 'https://demo.justcodeworks.eu/template1'
            },
            'industry_template_2': {
                'preview_image': 'https://via.placeholder.com/800x600/28a745/ffffff?text=Industry+Expert+Template',
                'thumbnail_image': 'https://via.placeholder.com/300x200/28a745/ffffff?text=Industry+Expert',
                'demo_url': 'https://demo.justcodeworks.eu/template2'
            },
            'modern_template_3': {
                'preview_image': 'https://via.placeholder.com/800x600/dc3545/ffffff?text=Modern+Corporate+Template',
                'thumbnail_image': 'https://via.placeholder.com/300x200/dc3545/ffffff?text=Modern+Corporate',
                'demo_url': 'https://demo.justcodeworks.eu/template3'
            }
        }
        
        updated_count = 0
        
        for template_id, images in template_previews.items():
            try:
                template = WebsiteTemplate.objects.get(template_id=template_id)
                template.preview_image = images['preview_image']
                template.thumbnail_image = images['thumbnail_image']
                template.demo_url = images['demo_url']
                template.save()
                
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Updated {template.name} with preview images')
                )
                updated_count += 1
                
            except WebsiteTemplate.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'⚠️ Template {template_id} not found')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n🎉 Successfully updated {updated_count} templates with preview images!')
        )
        
        # Show current templates with their images
        self.stdout.write(self.style.SUCCESS('\n📋 Current Templates:'))
        templates = WebsiteTemplate.objects.all().order_by('template_id')
        
        for template in templates:
            self.stdout.write(f'  • {template.name}')
            self.stdout.write(f'    Preview: {template.preview_image or "None"}')
            self.stdout.write(f'    Thumbnail: {template.thumbnail_image or "None"}')
            self.stdout.write(f'    Demo: {template.demo_url or "None"}')
            self.stdout.write('')