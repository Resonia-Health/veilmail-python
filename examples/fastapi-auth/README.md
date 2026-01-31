# FastAPI Auth Example with VeilMail

A FastAPI application demonstrating email verification, password reset, two-factor authentication, and security notification emails using the VeilMail Python SDK.

## Features

- **Email verification** on registration
- **Password reset** via email link
- **Two-factor authentication** with email codes
- **Security notifications** for password changes and 2FA toggles
- JWT-based authentication
- SQLite database via SQLModel

## Setup

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your VeilMail API key and settings
```

## Run

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000 with interactive docs at http://localhost:8000/docs.
