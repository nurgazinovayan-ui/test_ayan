import logging
from datetime import datetime
from sqlalchemy.orm import Session
from app.bot.telegram_bot import send_draft_preview
from app.integrations.instagram_client import InstagramClient
from app.integrations.openai_client import generate_content
from app.integrations.storage import upload_image
from app.models import Draft, DraftStatus
from app.services.image_service import generate_image

logger = logging.getLogger(__name__)


def create_draft_from_trends(db: Session, trend_summary: str) -> Draft:
    data = generate_content(trend_summary)
    choice = data['concepts'][0]
    local_image = generate_image(data['image_prompt'])
    public_url = upload_image(local_image)
    draft = Draft(
        concept=choice['concept'],
        rationale=choice['rationale'],
        caption=data['caption'],
        hashtags=data['hashtags'],
        image_prompt=data['image_prompt'],
        image_local_path=local_image,
        image_public_url=public_url,
        status=DraftStatus.draft,
        updated_at=datetime.utcnow(),
    )
    db.add(draft)
    db.commit()
    db.refresh(draft)
    send_draft_preview(draft.id, draft.image_public_url, f"{draft.caption}\n\n{draft.hashtags}")
    return draft


def publish_draft(db: Session, draft: Draft) -> Draft:
    client = InstagramClient()
    creation_id = client.create_media_container(draft.image_public_url, f"{draft.caption}\n\n{draft.hashtags}")
    post_id = client.publish_media(creation_id)
    draft.instagram_post_id = post_id
    draft.status = DraftStatus.published
    draft.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(draft)
    return draft
