"""
Management command to add template screenshots
Usage: python manage.py add_template_screenshots --template-id TP1 --preview screenshot.jpg --thumbnail thumb.jpg
"""
import os
import shutil
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from website_builder.models import WebsiteTemplate


class Command(BaseCommand):
    help = 'Add preview and thumbnail screenshots for website templates'

    def add_arguments(self, parser):
        parser.add_argument(
            '--template-id',
            type=str,
            required=True,
            help='Template ID (e.g., TP1, TP2, etc.)'
        )
        parser.add_argument(
            '--preview',
            type=str,
            help='Path to preview image file (will be copied to media/website_templates/previews/)'
        )
        parser.add_argument(
            '--thumbnail',
            type=str,
            help='Path to thumbnail image file (will be copied to media/website_templates/thumbnails/)'
        )
        parser.add_argument(
            '--preview-url',
            type=str,
            help='Direct URL for preview image (if already hosted)'
        )
        parser.add_argument(
            '--thumbnail-url',
            type=str,
            help='Direct URL for thumbnail image (if already hosted)'
        )

    def handle(self, *args, **options):
        template_id = options['template_id']
        
        try:
            template = WebsiteTemplate.objects.get(template_id=template_id)
        except WebsiteTemplate.DoesNotExist:
            raise CommandError(f'Template with ID "{template_id}" does not exist')

        # Create media directories if they don't exist
        preview_dir = os.path.join(settings.MEDIA_ROOT, 'website_templates', 'previews')
        thumbnail_dir = os.path.join(settings.MEDIA_ROOT, 'website_templates', 'thumbnails')
        os.makedirs(preview_dir, exist_ok=True)
        os.makedirs(thumbnail_dir, exist_ok=True)

        updated_fields = []

        # Handle preview image
        if options['preview']:
            preview_path = options['preview']
            if not os.path.exists(preview_path):
                raise CommandError(f'Preview image file does not exist: {preview_path}')
            
            # Get file extension
            _, ext = os.path.splitext(preview_path)
            if not ext.lower() in ['.jpg', '.jpeg', '.png', '.webp']:
                raise CommandError(f'Preview image must be JPG, PNG, or WebP format')
            
            # Copy to media directory
            new_filename = f'{template_id}_preview{ext}'
            destination = os.path.join(preview_dir, new_filename)
            shutil.copy2(preview_path, destination)
            
            # Update template
            template.preview_image = f'/media/website_templates/previews/{new_filename}'
            updated_fields.append('preview_image')
            self.stdout.write(f'Preview image copied to: {destination}')

        elif options['preview_url']:
            template.preview_image = options['preview_url']
            updated_fields.append('preview_image')
            self.stdout.write(f'Preview URL set to: {options["preview_url"]}')

        # Handle thumbnail image
        if options['thumbnail']:
            thumbnail_path = options['thumbnail']
            if not os.path.exists(thumbnail_path):
                raise CommandError(f'Thumbnail image file does not exist: {thumbnail_path}')
            
            # Get file extension
            _, ext = os.path.splitext(thumbnail_path)
            if not ext.lower() in ['.jpg', '.jpeg', '.png', '.webp']:
                raise CommandError(f'Thumbnail image must be JPG, PNG, or WebP format')
            
            # Copy to media directory
            new_filename = f'{template_id}_thumbnail{ext}'
            destination = os.path.join(thumbnail_dir, new_filename)
            shutil.copy2(thumbnail_path, destination)
            
            # Update template
            template.thumbnail_image = f'/media/website_templates/thumbnails/{new_filename}'
            updated_fields.append('thumbnail_image')
            self.stdout.write(f'Thumbnail image copied to: {destination}')

        elif options['thumbnail_url']:
            template.thumbnail_image = options['thumbnail_url']
            updated_fields.append('thumbnail_image')
            self.stdout.write(f'Thumbnail URL set to: {options["thumbnail_url"]}')

        if updated_fields:
            template.save(update_fields=updated_fields)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully updated template "{template.name}" ({template_id})'
                )
            )
            self.stdout.write(f'Updated fields: {", ".join(updated_fields)}')
            
            if template.preview_image:
                self.stdout.write(f'Preview: {template.preview_image}')
            if template.thumbnail_image:
                self.stdout.write(f'Thumbnail: {template.thumbnail_image}')
        else:
            self.stdout.write('No images provided. Use --preview, --thumbnail, --preview-url, or --thumbnail-url')