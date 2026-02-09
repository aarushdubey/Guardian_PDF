#!/usr/bin/env python3
"""
Quick test to verify NVIDIA API key is working.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment
load_dotenv()

print("🧪 Testing NVIDIA AI API Connection...")
print()

# Get API key
api_key = os.getenv("NVIDIA_API_KEY")

if not api_key:
    print("❌ NVIDIA_API_KEY not found in environment")
    print("   Make sure .env file exists and contains your API key")
    exit(1)

print(f"✅ API Key found: {api_key[:15]}...")
print()

# Test connection
try:
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=api_key
    )
    
    print("📡 Sending test request to NVIDIA AI...")
    
    completion = client.chat.completions.create(
        model="meta/llama3-70b-instruct",
        messages=[
            {
                "role": "user",
                "content": "Say 'Hello from GuardianPDF!' and nothing else."
            }
        ],
        max_tokens=50
    )
    
    response = completion.choices[0].message.content
    
    print("✅ Response received!")
    print()
    print(f"🤖 NVIDIA AI says: {response}")
    print()
    print("=" * 60)
    print("✅ SUCCESS! NVIDIA API is working correctly!")
    print("=" * 60)
    print()
    print("You're ready to use GuardianPDF with NVIDIA AI!")
    
except Exception as e:
    print("❌ Error connecting to NVIDIA API:")
    print(f"   {str(e)}")
    print()
    print("Troubleshooting:")
    print("  1. Verify your API key is correct")
    print("  2. Check internet connection")
    print("  3. Ensure API key has proper permissions")
    exit(1)
