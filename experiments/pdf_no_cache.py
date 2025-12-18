# python pdf_no_cache.py
 
import json
import io
import httpx
import time
from google import genai

# ===== Load API key =====
KEY_PATH = "/Users/shou-weilin/Desktop/Others/Project/CathayNew/google_gemini_api.json"
api_key = json.load(open(KEY_PATH))["gemini_api_key"]

client = genai.Client(api_key=api_key)
model_name = "gemini-2.0-flash-001"

# ===== Download PDF =====
pdf_url = "https://www.nasa.gov/wp-content/uploads/static/history/alsj/a17/A17_FlightPlan.pdf"
pdf_bytes = httpx.get(pdf_url).content
pdf_io = io.BytesIO(pdf_bytes)

# ===== MULTI-QUERY WITHOUT CACHE =====
questions = [
    "請用 5 點條列總結 Apollo 17 Flight Plan 的主要任務目標。",
    "這次任務與 Apollo 16 最大的差異是什麼？",
    "這份計畫中，太空人最重要的科學任務有哪些？",
]

print("\n=== NO CACHE : MULTI QUERY RUN ===")

for i, q in enumerate(questions, 1):
    print(f"\n--- Query {i} ---")

    # ⚠️ 每一次都重新 upload PDF
    pdf_io.seek(0)
    file = client.files.upload(
        file=pdf_io,
        config={"mime_type": "application/pdf"}
    )

    start = time.time()

    response = client.models.generate_content(
        model=model_name,
        contents=[
            file,  # ⚠️ 大量 tokens 每次重新 ingest
            q
        ]
    )

    latency = time.time() - start
    usage = response.usage_metadata

    print(f"Latency: {latency:.2f}s")
    print(
        f"Prompt tokens: {usage.prompt_token_count}, "
        f"Output tokens: {usage.candidates_token_count}, "
        f"Total: {usage.total_token_count}"
    )
