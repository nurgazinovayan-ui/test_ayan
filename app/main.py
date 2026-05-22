from fastapi import FastAPI
from app.api.routes import router
from app.core.logging import setup_logging
from app.db.base import Base
from app.db.session import engine
from app.workers.scheduler import start_scheduler

setup_logging()
app = FastAPI(title='Instagram AI Content Agent')
app.include_router(router)


@app.on_event('startup')
def startup() -> None:
    Base.metadata.create_all(bind=engine)
    start_scheduler()


@app.get('/health')
def health():
    return {'status': 'ok'}
