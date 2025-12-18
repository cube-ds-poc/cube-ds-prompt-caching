# python short_prompt_with_cache.py
import sys
import os
import json
from google import genai

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.timer import Timer
from utils.token_logger import print_usage

# Load API key
KEY_PATH = "/Users/shou-weilin/Desktop/Others/Project/CathayNew/google_gemini_api.json"
with open(KEY_PATH) as f:
    api_key = json.load(f)["gemini_api_key"]

# Client
client = genai.Client(api_key=api_key)

model_name = "gemini-2.0-flash-001"

# Long SOP rules — simulate a cached context
rules = "你是 Queue LLM Agent，需要遵守以下規則：\n1. 回覆需包含 RETURNCODE。\n2. 根據任務類型執行流程。\n" * 50

# Build combined prompt (rules + user prompt)
prompt = f"{rules}\n\n請回答任務是否完成？"

with Timer("Short Prompt - With Simulated Cache"):
    result = client.models.generate_content(
        model=model_name,
        contents=prompt
    )

print_usage(result.usage_metadata)
print("\nGenerated response:")
print(result.text)
