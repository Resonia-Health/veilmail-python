from veilmail import VeilMail
from app.config import VEILMAIL_API_KEY, VEILMAIL_FROM_EMAIL, APP_URL

client = VeilMail(api_key=VEILMAIL_API_KEY)


def send_verification_email(email: str, token: str):
    url = f"{APP_URL}/auth/verify-email?token={token}"
    client.emails.send(
        from_email=VEILMAIL_FROM_EMAIL,
        to=email,
        subject="Verify your email address",
        html=f'<p>Click <a href="{url}">here</a> to verify your email. This link expires in 1 hour.</p>',
        tags=["auth", "verification"],
        type="transactional",
    )


def send_password_reset_email(email: str, token: str):
    url = f"{APP_URL}/auth/reset-password?token={token}"
    client.emails.send(
        from_email=VEILMAIL_FROM_EMAIL,
        to=email,
        subject="Reset your password",
        html=f'<p>Click <a href="{url}">here</a> to reset your password. This link expires in 1 hour.</p>',
        tags=["auth", "password-reset"],
        type="transactional",
    )


def send_two_factor_code(email: str, code: str):
    client.emails.send(
        from_email=VEILMAIL_FROM_EMAIL,
        to=email,
        subject=f"{code} is your verification code",
        html=f"<p>Your two-factor authentication code is: <strong>{code}</strong></p><p>This code expires in 5 minutes.</p>",
        tags=["auth", "2fa"],
        type="transactional",
    )


def send_welcome_email(email: str, name: str):
    client.emails.send(
        from_email=VEILMAIL_FROM_EMAIL,
        to=email,
        subject="Welcome!",
        html=f"<p>Welcome{f', {name}' if name else ''}! Your email has been verified and your account is active.</p>",
        tags=["auth", "welcome"],
        type="transactional",
    )


def send_password_changed_email(email: str):
    client.emails.send(
        from_email=VEILMAIL_FROM_EMAIL,
        to=email,
        subject="Your password was changed",
        html="<p>Your password was successfully changed. If you didn't make this change, please reset your password immediately.</p>",
        tags=["auth", "security"],
        type="transactional",
    )


def send_two_factor_toggled_email(email: str, enabled: bool):
    status = "enabled" if enabled else "disabled"
    client.emails.send(
        from_email=VEILMAIL_FROM_EMAIL,
        to=email,
        subject=f"Two-factor authentication {status}",
        html=f"<p>Two-factor authentication has been {status} on your account.</p>",
        tags=["auth", "2fa", "security"],
        type="transactional",
    )
