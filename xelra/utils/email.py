"""Email utilities for OTP delivery.

Supports:
- Resend (recommended, modern transactional email API)
- SMTP (legacy fallback)
"""

import smtplib
from email.mime.text import MIMEText
import httpx

from ..config import settings


def send_otp_email(to_email: str, code: str) -> dict:
    """Send an OTP code via email.

    Tries Resend first, falls back to SMTP if not configured.

    Args:
        to_email: Recipient email address
        code: 6-digit OTP code

    Returns:
        dict with 'success' (bool), 'provider' (str), and optionally 'error' (str)
    """
    # Try Resend first
    if settings.resend_api_key:
        result = _send_via_resend(to_email, code)
        if result["success"]:
            return result
        # If Resend fails, try SMTP as fallback
        print(f"[email] Resend failed: {result.get('error')}, trying SMTP...")

    # Try SMTP
    if settings.smtp_host and settings.smtp_user and settings.smtp_pass:
        return _send_via_smtp(to_email, code)

    # No email provider configured
    return {
        "success": False,
        "provider": "none",
        "error": "No email provider configured (set RESEND_API_KEY or SMTP settings)",
    }


def _send_via_resend(to_email: str, code: str) -> dict:
    """Send email via Resend API."""
    if not settings.resend_api_key:
        return {"success": False, "provider": "resend", "error": "API key not configured"}

    subject = "Your X-ELRA Sign-in Code"

    html_content = f"""
    <div style="font-family: system-ui, -apple-system, sans-serif; max-width: 480px; margin: 0 auto; padding: 24px;">
        <h2 style="color: #111; margin-bottom: 8px;">Your verification code</h2>
        <p style="color: #666; margin-bottom: 24px;">
            Use this code to sign in to X-ELRA. It expires in 15 minutes.
        </p>
        <div style="background: #f3f4f6; border-radius: 8px; padding: 24px; text-align: center; margin-bottom: 24px;">
            <span style="font-size: 32px; font-weight: bold; letter-spacing: 8px; color: #111;">{code}</span>
        </div>
        <p style="color: #999; font-size: 14px;">
            If you didn't request this code, you can safely ignore this email.
        </p>
    </div>
    """

    text_content = f"""Your X-ELRA verification code is: {code}

Use this code to sign in. It expires in 15 minutes.

If you didn't request this code, you can safely ignore this email."""

    try:
        response = httpx.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {settings.resend_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "from": settings.resend_from_email,
                "to": [to_email],
                "subject": subject,
                "html": html_content,
                "text": text_content,
            },
            timeout=10.0,
        )

        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "provider": "resend",
                "message_id": data.get("id"),
            }
        else:
            error_data = response.json() if response.content else {}
            return {
                "success": False,
                "provider": "resend",
                "error": error_data.get("message", f"HTTP {response.status_code}"),
            }

    except httpx.TimeoutException:
        return {"success": False, "provider": "resend", "error": "Request timeout"}
    except Exception as e:
        return {"success": False, "provider": "resend", "error": str(e)}


def _send_via_smtp(to_email: str, code: str) -> dict:
    """Send email via SMTP (legacy fallback)."""
    if not settings.smtp_host or not settings.smtp_user or not settings.smtp_pass:
        return {"success": False, "provider": "smtp", "error": "SMTP not configured"}

    subject = "Your X-ELRA Sign-in Code"
    body = f"Your X-ELRA verification code is {code}.\n\nUse this code to sign in. It expires in 15 minutes."

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = settings.smtp_from
    msg["To"] = to_email

    try:
        if settings.smtp_use_tls:
            server = smtplib.SMTP(settings.smtp_host, settings.smtp_port)
            server.starttls()
        else:
            server = smtplib.SMTP(settings.smtp_host, settings.smtp_port)

        server.login(settings.smtp_user, settings.smtp_pass)
        server.send_message(msg)
        server.quit()

        return {"success": True, "provider": "smtp"}

    except Exception as e:
        return {"success": False, "provider": "smtp", "error": str(e)}
