#!/usr/bin/env python
"""
Test script to debug business name detection
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'justcodeworks.settings')
django.setup()

from website_builder.clippy_assistant import ClippyWebsiteBuilder

# Test the detection
clippy = ClippyWebsiteBuilder()

test_names = [
    "ABC Construction",
    "Jo's Tyres", 
    "Smith Dental Practice",
    "Mike's Auto Repair",
    "Bella's Beauty Salon",
    "Bobby Tom",
    "John Smith",
    "Mary Johnson",
    "Tech Solutions Inc",
    "General Business"
]

print("🔍 Testing Business Name Detection:")
print("=" * 50)

for name in test_names:
    detected = clippy._detect_industry(name.lower())
    print(f"📝 '{name}' → {detected}")
    
print("\n✅ Detection test complete!")