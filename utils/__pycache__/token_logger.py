def print_usage(usage):
    if usage is None:
        print("No usage metadata returned.")
        return

    print("\n=== Token Usage ===")
    print(f"- prompt_token_count:      {usage.prompt_token_count}")
    print(f"- candidates_token_count:  {usage.candidates_token_count}")
    print(f"- total_token_count:       {usage.total_token_count}")
    print("====================\n")
