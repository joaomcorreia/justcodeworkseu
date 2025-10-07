#!/usr/bin/env python
"""
Test multi-industry detection for "Joly's Window Washing and Paint"
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'justcodeworks.settings')
django.setup()

from website_builder.clippy_assistant import ClippyWebsiteBuilder

clippy = ClippyWebsiteBuilder()

test_names = [
    "Joly's Window Washing and Paint",
    "ABC Plumbing and Electrical", 
    "Mike's Auto Repair and Tires",
    "Smith Dental and Medical Practice",
    "Bob's Cleaning and Pest Control"
]

print("🔍 Testing Multi-Industry Detection:")
print("=" * 50)

for name in test_names:
    detected = clippy._detect_industry(name.lower())
    print(f"📝 '{name}' → {detected}")

print("\n✅ Current detection complete!")