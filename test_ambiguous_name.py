#!/usr/bin/env python
"""
Test script to simulate the conversation flow for Bobby Tom (ambiguous name)
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
user, _ = User.objects.get_or_create(username='testuser2', defaults={'email': 'test2@test.com'})

# Create a new project and conversation
project = WebsiteProject.objects.create(
    user=user,
    business_name="Test Project 2"
)

conversation = WebsiteBuilderConversation.objects.create(
    project=project,
    current_step='business_name',
    conversation_data={}
)

# Create Clippy instance
clippy = ClippyWebsiteBuilder()

print("🤖 Testing Clippy 2.0 with Ambiguous Business Name")
print("=" * 60)
print("\n📝 Step 1: Testing business name input 'Bobby Tom'")

# Simulate entering "Bobby Tom" as business name (should be ambiguous)
response = clippy._step_business_name(conversation, "Bobby Tom")

print(f"🔄 Current step after business name: {conversation.current_step}")
print(f"📊 Conversation data: {conversation.conversation_data}")
print(f"🏢 Project industry: {conversation.project.industry}")
print(f"💬 Clippy's response:")
print("-" * 50)
print(response)
print("-" * 50)

# Test if it correctly goes to industry selection instead of services
if conversation.current_step == 'industry_selection':
    print("\n✅ SUCCESS: Ambiguous name correctly triggers industry selection!")
else:
    print(f"\n❌ ERROR: Expected 'industry_selection', got '{conversation.current_step}'")

print("\n🔄 Testing clear industry input...")
# Now simulate selecting "restaurant" as industry
response2 = clippy._step_industry_selection(conversation, "restaurant")
print(f"🔄 Current step after industry: {conversation.current_step}")
print(f"💬 Clippy's response for restaurant:")
print("-" * 50)
print(response2[:300] + "..." if len(response2) > 300 else response2)
print("-" * 50)

print("\n✅ Complete test finished!")