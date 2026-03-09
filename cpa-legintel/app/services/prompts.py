def law_impact_prompt(
    client_name: str,
    client_state: str,
    entity_type: str,
    law_text: str,
) -> str:
    return f"""
You are a regulatory compliance analyst.

Client:
- Name: {client_name}
- Entity type: {entity_type}
- State: {client_state}

Law text:
{law_text}

Task:
1. Determine whether this law is likely to affect the client.
2. Summarize the impact in plain English.
3. Provide a confidence score between 0 and 1.

Respond in JSON with:
- summary
- reasoning
- confidence
""".strip()
