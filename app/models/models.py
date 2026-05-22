import enum
from datetime import datetime
from sqlalchemy import DateTime, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class DraftStatus(str, enum.Enum):
    draft = 'draft'
    approved = 'approved'
    rejected = 'rejected'
    published = 'published'
    failed = 'failed'


class TrendPost(Base):
    __tablename__ = 'trend_posts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    source: Mapped[str] = mapped_column(String(64))
    source_identifier: Mapped[str] = mapped_column(String(128), index=True)
    caption: Mapped[str] = mapped_column(Text, default='')
    media_url: Mapped[str] = mapped_column(Text, default='')
    posted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    likes: Mapped[int] = mapped_column(Integer, default=0)
    comments: Mapped[int] = mapped_column(Integer, default=0)
    views: Mapped[int] = mapped_column(Integer, default=0)
    trend_score: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)


class Draft(Base):
    __tablename__ = 'drafts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    concept: Mapped[str] = mapped_column(Text)
    rationale: Mapped[str] = mapped_column(Text)
    caption: Mapped[str] = mapped_column(Text)
    hashtags: Mapped[str] = mapped_column(Text)
    image_prompt: Mapped[str] = mapped_column(Text)
    image_local_path: Mapped[str] = mapped_column(Text, default='')
    image_public_url: Mapped[str] = mapped_column(Text, default='')
    status: Mapped[DraftStatus] = mapped_column(Enum(DraftStatus), default=DraftStatus.draft)
    review_note: Mapped[str] = mapped_column(Text, default='')
    instagram_post_id: Mapped[str] = mapped_column(String(128), default='')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    analytics: Mapped[list['Analytics']] = relationship(back_populates='draft')


class Analytics(Base):
    __tablename__ = 'analytics'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    draft_id: Mapped[int] = mapped_column(ForeignKey('drafts.id', ondelete='CASCADE'))
    impressions: Mapped[int] = mapped_column(Integer, default=0)
    reach: Mapped[int] = mapped_column(Integer, default=0)
    likes: Mapped[int] = mapped_column(Integer, default=0)
    comments: Mapped[int] = mapped_column(Integer, default=0)
    saves: Mapped[int] = mapped_column(Integer, default=0)
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    draft: Mapped[Draft] = relationship(back_populates='analytics')
