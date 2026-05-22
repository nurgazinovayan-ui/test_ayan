import httpx
from app.core.config import get_settings

settings = get_settings()


def send_draft_preview(draft_id: int, image_url: str, text: str) -> None:
    if not settings.telegram_bot_token or not settings.telegram_chat_id:
        return
    keyboard = {
        'inline_keyboard': [[
            {'text': 'Approve', 'callback_data': f'approve:{draft_id}'},
            {'text': 'Reject', 'callback_data': f'reject:{draft_id}'},
            {'text': 'Regenerate', 'callback_data': f'regenerate:{draft_id}'},
        ]]
    }
    httpx.post(
        f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendPhoto",
        data={
            'chat_id': settings.telegram_chat_id,
            'photo': image_url,
            'caption': text[:1024],
            'reply_markup': __import__('json').dumps(keyboard),
        },
        timeout=30,
    )
