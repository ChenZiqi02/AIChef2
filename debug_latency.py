import time
import sys
import os

# Improve import path handling
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from core.generator import safe_invoke
    print("Testing LLM Latency...")
except ImportError as e:
    print(f"Import failed: {e}")
    sys.exit(1)

messages = [
    ("system", "You are a helpful assistant."),
    ("human", "Say 'Test' and nothing else.")
]

print("Sending request to SiliconFlow/DeepSeek...")
start_time = time.time()
try:
    response = safe_invoke(messages)
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"Response received in {duration:.2f} seconds")
    print(f"Content: {response.content}")
except Exception as e:
    print(f"Invocation failed after {time.time() - start_time:.2f} seconds with error: {e}")
