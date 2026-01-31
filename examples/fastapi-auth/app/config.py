import os

SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./auth.db")
VEILMAIL_API_KEY = os.getenv("VEILMAIL_API_KEY", "")
VEILMAIL_FROM_EMAIL = os.getenv("VEILMAIL_FROM_EMAIL", "noreply@veilmail.xyz")
APP_URL = os.getenv("APP_URL", "http://localhost:8000")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"
