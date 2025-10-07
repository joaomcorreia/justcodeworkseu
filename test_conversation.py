#!/usr/bin/env python
"""
Test script to simulate the conversation flow for ABC Construction
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
user, _ = User.objects.get_or_create(username='testuser', defaults={'email': 'test@test.com'})

# Create a new project and conversation
project = WebsiteProject.objects.create(
    user=user,
    business_name="Test Project"
)

conversation = WebsiteBuilderConversation.objects.create(
    project=project,
    current_step='business_name',
    conversation_data={}
)

# Create Clippy instance
clippy = ClippyWebsiteBuilder()

print("🤖 Testing Clippy 2.0 Conversation Flow")
print("=" * 50)
print("\n📝 Step 1: Testing business name input 'ABC Construction'")

# Simulate entering "ABC Construction" as business name
response = clippy._step_business_name(conversation, "ABC Construction")

print(f"🔄 Current step after business name: {conversation.current_step}")
print(f"📊 Conversation data: {conversation.conversation_data}")
print(f"🏢 Project industry: {conversation.project.industry}")
print(f"💬 Clippy's response:")
print("-" * 30)
print(response)
print("-" * 30)

print("\n✅ Test complete!")