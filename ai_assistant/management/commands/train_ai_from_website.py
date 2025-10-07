"""
Management command to train AI assistant by reading website pages
"""
from django.core.management.base import BaseCommand
from ai_assistant.magic_ai import magic_ai


class Command(BaseCommand):
    help = 'Train AI assistant by reading website pages'

    def add_arguments(self, parser):
        parser.add_argument(
            '--url',
            type=str,
            help='Base URL to crawl (e.g., http://127.0.0.1:8000). If not provided, reads static files directly.'
        )
        parser.add_argument(
            '--static-only',
            action='store_true',
            help='Only read static HTML files from filesystem (default behavior)'
        )

    def handle(self, *args, **options):
        self.stdout.write('🤖 Training AI assistant by reading website pages...')
        
        base_url = options.get('url')
        
        if base_url:
            self.stdout.write(f'📡 Crawling website at: {base_url}')
            success = magic_ai.crawl_website_pages(base_url)
        else:
            self.stdout.write('📄 Reading static HTML files from filesystem...')
            success = magic_ai.crawl_website_pages()  # No URL = read static files
        
        if success:
            self.stdout.write(
                self.style.SUCCESS('✅ Successfully trained AI with website content!')
            )
            self.stdout.write('💡 Your AI assistant can now answer questions about:')
            self.stdout.write('   - Your services and pricing')
            self.stdout.write('   - Company information')
            self.stdout.write('   - Contact details')
            self.stdout.write('   - Privacy policy and terms')
            self.stdout.write('')
            self.stdout.write('🎯 Test your AI by going to the admin dashboard and chatting with it!')
        else:
            self.stdout.write(
                self.style.ERROR('❌ Failed to train AI assistant. Check logs for details.')
            )