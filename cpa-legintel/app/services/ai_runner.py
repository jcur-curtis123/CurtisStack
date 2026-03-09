def run_llm(client_id, law_version_id, prompt):
    enforce_budget(client_id)
    result = llm(prompt)
    log_ai_usage(...)
    return result
