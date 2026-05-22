import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.core.config import get_settings
from app.db.session import SessionLocal
from app.services.draft_service import create_draft_from_trends
from app.services.trend_service import collect_trends

logger = logging.getLogger(__name__)
settings = get_settings()
scheduler = BackgroundScheduler()


def daily_pipeline() -> None:
    db = SessionLocal()
    try:
        trend_posts = collect_trends(db, settings.hashtags_list, settings.competitor_accounts_list)
        top = sorted(trend_posts, key=lambda x: x.trend_score, reverse=True)[:5]
        summary = '\n'.join([f"{t.source}:{t.source_identifier}:{t.caption}" for t in top])
        create_draft_from_trends(db, summary)
        logger.info('Daily pipeline complete')
    except Exception:
        logger.exception('Daily pipeline failed')
    finally:
        db.close()


def start_scheduler() -> None:
    minute, hour, *_ = settings.schedule_cron.split()
    scheduler.add_job(daily_pipeline, CronTrigger(minute=minute, hour=hour), id='daily_pipeline', replace_existing=True)
    scheduler.start()
