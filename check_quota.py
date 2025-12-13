import os
import time
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

models = [
    "gemini-2.0-flash", 
    "gemini-2.0-flash-lite-preview-02-05", # Try the new lite model
    "gemini-flash-latest",
    "gemini-1.5-flash"
]

print(f"🔑 Testing API Key: {api_key[:5]}...")

for model in models:
    print(f"\n👉 Testing Model: {model}")
    try:
        llm = ChatGoogleGenerativeAI(model=model, google_api_key=api_key)
        res = llm.invoke("Hello, are you alive?")
        print(f"✅ SUCCESS: {res.content}")
        break # Found a working one!
    except Exception as e:
        print(f"❌ FAILED: {e}")
        if "429" in str(e):
            print("   (Quota Exhausted)")
