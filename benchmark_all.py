# benchmark_all.py
"""
Run 4 experiments:
1. short_prompt_no_cache
2. short_prompt_with_cache
3. long_prompt_no_cache
4. long_prompt_with_cache

Collect:
- total time
- input_tokens
- output_tokens
- cached_content_used (Y/N)

Output:
- Markdown table (可直接貼在簡報)
- 保存到 benchmark_results.json
"""

import json
import subprocess
import time
from pathlib import Path

EXPERIMENTS = [
    ("short_prompt_no_cache", "experiments/short_prompt_no_cache.py"),
    ("short_prompt_with_cache", "experiments/short_prompt_with_cache.py"),
    ("long_prompt_no_cache", "experiments/long_prompt_no_cache.py"),
    ("long_prompt_with_cache", "experiments/long_prompt_with_cache.py"),
]

RESULT_PATH = Path("benchmark_results.json")


def run_script(label, file_path):
    print(f"\n🚀 Running {label} ...")

    start = time.time()

    proc = subprocess.Popen(
        ["python", file_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    stdout, stderr = proc.communicate()
    end = time.time()

    elapsed = round(end - start, 3)

    print("⏱ Time:", elapsed, "sec")
    if stderr.strip():
        print("⚠ stderr:", stderr)

    # 抓 usage_metadata JSON（透過 token_logger.py）
    usage = None
    for line in stdout.splitlines():
        if line.startswith("USAGE_JSON:"):
            try:
                usage = json.loads(line.replace("USAGE_JSON:", "").strip())
            except:
                pass

    return {
        "label": label,
        "time_sec": elapsed,
        "usage": usage,
    }


def build_markdown(results):
    md = []
    md.append("| Test Case | Time (sec) | Input Tokens | Output Tokens | Cached? |")
    md.append("|-----------|------------|--------------|---------------|---------|")

    for r in results:
        usage = r["usage"] or {}
        cached = "Yes" if usage.get("cached_content", False) else "No"
        md.append(
            f"| {r['label']} "
            f"| {r['time_sec']} "
            f"| {usage.get('input_tokens', 0)} "
            f"| {usage.get('output_tokens', 0)} "
            f"| {cached} |"
        )
    return "\n".join(md)


if __name__ == "__main__":
    print("====== Gemini Prompt Caching Benchmark ======")

    all_results = []

    for label, path in EXPERIMENTS:
        r = run_script(label, path)
        all_results.append(r)

    # 存結果
    with open(RESULT_PATH, "w") as f:
        json.dump(all_results, f, indent=2)

    print("\n📦 Saved results → benchmark_results.json\n")

    # 印 markdown 表
    md = build_markdown(all_results)
    print("\n====== Markdown Summary ======\n")
    print(md)
    print("\n================================\n")

    # 方便你直接貼進簡報
    with open("benchmark_summary.md", "w") as f:
        f.write(md)

    print("✨ benchmark_summary.md generated!")
