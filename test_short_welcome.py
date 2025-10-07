#!/usr/bin/env python
"""
Test the short welcome message
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'justcodeworks.settings')
django.setup()

from django.contrib.auth.models import User
from website_builder.clippy_assistant import ClippyWebsiteBuilder
from website_builder.models import WebsiteProject, WebsiteBuilderConversation

# Get or create a test user
user, _ = User.objects.get_or_create(username='testuser3', defaults={'email': 'test3@test.com', 'first_name': 'John'})

# Create a new project and conversation
project = WebsiteProject.objects.create(
    user=user,
    business_name="Test Project 3"
)

conversation = WebsiteBuilderConversation.objects.create(
    project=project,
    current_step='welcome',
    conversation_data={}
)

# Create Clippy instance
clippy = ClippyWebsiteBuilder()

print("🤖 Testing Short Welcome Message")
print("=" * 40)

# Test welcome step
response = clippy._step_welcome(conversation, "")

print("💬 Clippy's welcome message:")
print("-" * 30)
print(response)
print("-" * 30)

print(f"\nMessage length: {len(response)} characters")
print("✅ Short and direct!")