class ClientAIBudget(Base):
    __tablename__ = "client_ai_budgets"

    client_id = Column(UUID, primary_key=True)
    daily_usd_limit = Column(Float)
    monthly_usd_limit = Column(Float)
