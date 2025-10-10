from django.core.management.base import BaseCommand
from website_builder.models import WebsiteTemplate


class Command(BaseCommand):
    help = 'Update template categories easily'

    def add_arguments(self, parser):
        parser.add_argument(
            '--from-category',
            type=str,
            help='Category to change from'
        )
        parser.add_argument(
            '--to-category', 
            type=str,
            help='Category to change to'
        )
        parser.add_argument(
            '--template-id',
            type=str,
            help='Specific template ID to update'
        )
        parser.add_argument(
            '--list',
            action='store_true',
            help='List all templates and their categories'
        )

    def handle(self, *args, **options):
        if options['list']:
            self.list_templates()
            return

        if options['template_id']:
            self.update_single_template(options['template_id'], options['to_category'])
        elif options['from_category'] and options['to_category']:
            self.update_category(options['from_category'], options['to_category'])
        else:
            self.stdout.write(
                self.style.ERROR('Please provide either --template-id or both --from-category and --to-category')
            )
            self.stdout.write('Use --list to see all templates')

    def list_templates(self):
        """List all templates and their categories"""
        templates = WebsiteTemplate.objects.all().order_by('category', 'template_id')
        
        self.stdout.write(
            self.style.SUCCESS('\n📋 All Templates and Categories:')
        )
        
        current_category = None
        for template in templates:
            if current_category != template.category:
                current_category = template.category
                self.stdout.write(f'\n🏷️  {template.category.upper()}:')
            
            self.stdout.write(f'   • {template.template_id} - {template.name}')
        
        # Show category counts
        categories = WebsiteTemplate.objects.values_list('category', flat=True).distinct()
        self.stdout.write('\n📊 Category Summary:')
        for cat in sorted(categories):
            count = WebsiteTemplate.objects.filter(category=cat).count()
            self.stdout.write(f'   • {cat}: {count} templates')

    def update_single_template(self, template_id, new_category):
        """Update a specific template's category"""
        try:
            template = WebsiteTemplate.objects.get(template_id=template_id)
            old_category = template.category
            template.category = new_category
            template.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Updated {template_id}: {old_category} → {new_category}')
            )
        except WebsiteTemplate.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'❌ Template {template_id} not found')
            )

    def update_category(self, from_category, to_category):
        """Update all templates from one category to another"""
        templates = WebsiteTemplate.objects.filter(category=from_category)
        count = templates.count()
        
        if count == 0:
            self.stdout.write(
                self.style.WARNING(f'⚠️  No templates found with category "{from_category}"')
            )
            return
        
        templates.update(category=to_category)
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Updated {count} templates: {from_category} → {to_category}')
        )
        
        # List updated templates
        updated_templates = WebsiteTemplate.objects.filter(category=to_category)
        for template in updated_templates:
            self.stdout.write(f'   • {template.template_id} - {template.name}')