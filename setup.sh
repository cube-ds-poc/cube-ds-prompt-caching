#!/bin/bash

echo "Creating project structure: xxx-prompt-caching/"

# === Create folders ===
mkdir -p experiments
mkdir -p utils
mkdir -p data

# === Create files ===
touch experiments/short_prompt_no_cache.py
touch experiments/short_prompt_with_cache.py
touch experiments/long_prompt_no_cache.py
touch experiments/long_prompt_with_cache.py

touch utils/timer.py
touch utils/token_logger.py

touch data/memory_hook_sample.json

touch README.md
touch requirements.txt

echo "All folders and files created!"
echo "You can now paste the Python scripts into the correct files."


