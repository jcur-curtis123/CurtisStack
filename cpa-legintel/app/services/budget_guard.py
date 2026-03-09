def enforce_budget(client_id):
    spent_today = ...
    if spent_today >= daily_limit:
        raise HTTPException(402, "AI budget exceeded")
