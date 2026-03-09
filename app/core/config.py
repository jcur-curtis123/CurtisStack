# app/core/config.py

import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")  # change before deploy
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
