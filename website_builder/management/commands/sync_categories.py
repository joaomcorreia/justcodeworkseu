from django.core.management.base import BaseCommand
from website_builder.models import WebsiteTemplate
import os


class Command(BaseCommand):
    help = 'Check and sync category names between database and views.py'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fix',
            action='store_true',
            help='Automatically update views.py with missing categories'
        )

    def handle(self, *args, **options):
        # Get categories from database
        db_categories = list(WebsiteTemplate.objects.filter(is_active=True).values_list('category', flat=True).distinct())
        
        # Try to read current category_names from views.py
        views_path = 'website_builder/views.py'
        try:
            with open(views_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract category_names dictionary (simple parsing)
            start_marker = "category_names = {"
            end_marker = "}"
            
            start_idx = content.find(start_marker)
            if start_idx == -1:
                self.stdout.write(self.style.ERROR("Could not find category_names dictionary in views.py"))
                return
            
            end_idx = content.find(end_marker, start_idx) + 1
            category_dict_text = content[start_idx:end_idx]
            
            # Extract existing categories (simple regex-like parsing)
            import re
            pattern = r"'(\w+)':\s*'[^']+'"
            existing_categories = re.findall(pattern, category_dict_text)
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error reading views.py: {e}"))
            return
        
        # Compare categories
        missing_in_views = [cat for cat in db_categories if cat not in existing_categories]
        unused_in_views = [cat for cat in existing_categories if cat not in db_categories]
        
        # Display results
        self.stdout.write(self.style.SUCCESS('\n📊 Category Sync Status:'))
        
        self.stdout.write(f'\n🗃️  Database Categories ({len(db_categories)}):')
        for cat in sorted(db_categories):
            count = WebsiteTemplate.objects.filter(category=cat).count()
            status = "✅" if cat in existing_categories else "❌"
            self.stdout.write(f'   {status} {cat} ({count} templates)')
        
        self.stdout.write(f'\n📝 Views.py Categories ({len(existing_categories)}):')
        for cat in sorted(existing_categories):
            status = "✅" if cat in db_categories else "⚠️ "
            self.stdout.write(f'   {status} {cat}')
        
        if missing_in_views:
            self.stdout.write(f'\n❌ Missing in views.py: {missing_in_views}')
            
        if unused_in_views:
            self.stdout.write(f'\n⚠️  Unused in views.py: {unused_in_views}')
        
        if not missing_in_views and not unused_in_views:
            self.stdout.write(self.style.SUCCESS('\n✅ All categories are in sync!'))
        
        # Auto-fix option
        if options['fix'] and missing_in_views:
            self.stdout.write('\n🔧 Auto-fixing category_names...')
            
            # Suggest emoji mappings for new categories
            emoji_suggestions = {
                'bars': '🍺',
                'business': '💼', 
                'creative': '🎨',
                'portfolio': '📁',
                'restaurant': '🍽️',
                'construction': '🏗️',
                'technology': '💻',
                'health': '🏥',
                'ecommerce': '🛒',
                'fashion': '👗',
                'sports': '⚽',
                'education': '📚',
                'travel': '✈️',
            }
            
            # Generate new category_names dictionary
            new_dict_lines = ['    # Category display name mapping (matches database categories)']
            new_dict_lines.append('    category_names = {')
            
            for cat in sorted(db_categories):
                emoji = emoji_suggestions.get(cat, '📂')
                display_name = f"{emoji} {cat.title()}"
                if cat == 'ecommerce':
                    display_name = f"{emoji} E-commerce"
                elif cat == 'portfolio':
                    display_name = f"{emoji} Portfolio & Showcase"
                elif cat == 'restaurant':
                    display_name = f"{emoji} Restaurant & Food"
                elif cat == 'business':
                    display_name = f"{emoji} Business & Professional"
                elif cat == 'creative':
                    display_name = f"{emoji} Creative & Design"
                elif cat == 'bars':
                    display_name = f"{emoji} Bars & Nightlife"
                
                new_dict_lines.append(f"        '{cat}': '{display_name}',")
            
            new_dict_lines.append('    }')
            
            self.stdout.write('\nSuggested category_names dictionary:')
            for line in new_dict_lines:
                self.stdout.write(line)
            
            self.stdout.write(self.style.WARNING('\n⚠️  Remember to manually update views.py with these changes!'))