"""
Simple script to test if OpenAI API key is working
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

print(f"Testing OpenAI API Key...")
print(f"Key starts with: {api_key[:20]}..." if api_key else "No API key found!")
print("-" * 50)

try:
    client = OpenAI(api_key=api_key)
    
    # Make a simple test call
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Say 'API key is working!' if you can read this."}
        ],
        max_tokens=20
    )
    
    result = response.choices[0].message.content
    print(f"✅ SUCCESS! OpenAI responded: {result}")
    print(f"✅ Your API key is working correctly!")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    print("\nCommon issues:")
    print("1. Insufficient quota - Add credits at https://platform.openai.com/account/billing")
    print("2. Invalid API key - Check your key at https://platform.openai.com/api-keys")
    print("3. Network issues - Check your internet connection")

print("-" * 50)
