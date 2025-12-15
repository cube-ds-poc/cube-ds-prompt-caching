import sys
import os
import json
import io
import httpx
from google import genai

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.timer import Timer
from utils.token_logger import print_usage

# Load key
KEY_PATH = "/Users/shou-weilin/Desktop/Others/Project/CathayNew/google_gemini_api.json"
with open(KEY_PATH) as f:
    api_key = json.load(f)["gemini_api_key"]

client = genai.Client(api_key=api_key)
model_name = "gemini-2.0-flash-001"

# Download PDF for long context (simulate long memory)
pdf_url = "https://www.nasa.gov/wp-content/uploads/static/history/alsj/a17/A17_FlightPlan.pdf"
pdf_bytes = httpx.get(pdf_url).content
long_context = f"PDF Content: {len(pdf_bytes)} bytes.\n" * 50

# Build full prompt (simulate cache by prepending)
prompt = long_context + "\n請總結 PDF 的主要內容。"

with Timer("Long Prompt - With Simulated Cache"):
    result = client.models.generate_content(
        model=model_name,
        contents=prompt
    )

print_usage(result.usage_metadata)
print("\nGenerated response:")
print(result.text)
