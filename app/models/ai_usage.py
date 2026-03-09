class AIUsageLog(Base):
    __tablename__ = "ai_usage_logs"

    id = Column(UUID, primary_key=True)
    client_id = Column(UUID, index=True)
    law_version_id = Column(UUID, index=True)
    model = Column(String)
    prompt_tokens = Column(Integer)
    completion_tokens = Column(Integer)
    cost_usd = Column(Float)
