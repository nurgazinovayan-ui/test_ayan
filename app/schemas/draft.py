from datetime import datetime
from pydantic import BaseModel
from app.models import DraftStatus


class DraftOut(BaseModel):
    id: int
    concept: str
    rationale: str
    caption: str
    hashtags: str
    image_public_url: str
    status: DraftStatus
    instagram_post_id: str
    created_at: datetime

    class Config:
        from_attributes = True
