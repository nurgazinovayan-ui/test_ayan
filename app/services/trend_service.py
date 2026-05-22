from datetime import datetime
from sqlalchemy.orm import Session
from app.models import TrendPost


def compute_trend_score(likes: int, comments: int, views: int) -> float:
    return round(likes * 1.0 + comments * 2.0 + views * 0.1, 2)


def collect_trends(db: Session, hashtags: list[str], accounts: list[str]) -> list[TrendPost]:
    # MVP fallback: stores placeholders when official API endpoints are not configured for discovery scope.
    posts: list[TrendPost] = []
    for tag in hashtags:
        likes, comments, views = 50, 12, 900
        item = TrendPost(
            source='hashtag',
            source_identifier=tag,
            caption=f'Trend sample for #{tag}',
            media_url='https://example.com/sample.jpg',
            posted_at=datetime.utcnow(),
            likes=likes,
            comments=comments,
            views=views,
            trend_score=compute_trend_score(likes, comments, views),
        )
        db.add(item)
        posts.append(item)
    for account in accounts:
        likes, comments, views = 80, 20, 1200
        item = TrendPost(
            source='account',
            source_identifier=account,
            caption=f'Competitor trend sample @{account}',
            media_url='https://example.com/sample2.jpg',
            posted_at=datetime.utcnow(),
            likes=likes,
            comments=comments,
            views=views,
            trend_score=compute_trend_score(likes, comments, views),
        )
        db.add(item)
        posts.append(item)
    db.commit()
    return posts
