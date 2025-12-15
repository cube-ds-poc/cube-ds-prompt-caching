# python short_prompt_no_cache.py

import sys
import os
import json
from google import genai   # Correct import for the new SDK

# Add project root to sys.path (good, keeps it working from experiments/)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.timer import Timer
from utils.token_logger import print_usage

# Load API key
KEY_PATH = "/Users/shou-weilin/Desktop/Others/Project/CathayNew/google_gemini_api.json"
with open(KEY_PATH) as f:
    api_key = json.load(f)["gemini_api_key"]

# Create client (this is the new way)
client = genai.Client(api_key=api_key)  # Explicitly pass the key, or set env var

# Model name — use a stable, widely available one
model_name = "gemini-2.0-flash-001"  # This exists and should work

# Or try these safe alternatives if you hit model issues:
# model_name = "gemini-2.0-flash"        # Alias for latest 2.0 Flash
# model_name = "gemini-2.5-flash"        # Newer, very fast

prompt = """
你是 Queue LLM Agent，需要遵守以下規則：
1. 回覆需包含 RETURNCODE。
2. 根據任務類型執行流程。
"""

with Timer("Short Prompt - No Cache"):
    result = client.models.generate_content(
        model=model_name,
        contents=prompt
    )

# Print token usage (now works with updated print_usage)
print_usage(result.usage_metadata)

# Print generated text
print("\nGenerated response:")
print(result.text)