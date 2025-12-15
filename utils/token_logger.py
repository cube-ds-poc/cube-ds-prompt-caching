# utils/token_logger.py

def print_usage(usage_metadata):
    if usage_metadata is None:
        print("No usage metadata available.")
        return
    
    print(f"Prompt tokens:     {usage_metadata.prompt_token_count}")
    print(f"Output tokens:     {usage_metadata.candidates_token_count}")
    print(f"Total tokens:      {usage_metadata.total_token_count}")
    
    # Some newer models also report thinking tokens (if applicable)
    if hasattr(usage_metadata, "thoughts_token_count"):
        print(f"Thinking tokens:   {usage_metadata.thoughts_token_count}")