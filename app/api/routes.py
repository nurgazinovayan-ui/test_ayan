from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import Draft, DraftStatus
from app.schemas.draft import DraftOut
from app.services.draft_service import create_draft_from_trends, publish_draft

router = APIRouter()


@router.get('/drafts', response_model=list[DraftOut])
def list_drafts(db: Session = Depends(get_db)):
    return db.query(Draft).order_by(Draft.created_at.desc()).all()


@router.get('/drafts/{draft_id}', response_model=DraftOut)
def get_draft(draft_id: int, db: Session = Depends(get_db)):
    draft = db.get(Draft, draft_id)
    if not draft:
        raise HTTPException(status_code=404, detail='Draft not found')
    return draft


@router.post('/drafts/{draft_id}/approve', response_model=DraftOut)
def approve_draft(draft_id: int, db: Session = Depends(get_db)):
    draft = db.get(Draft, draft_id)
    if not draft:
        raise HTTPException(status_code=404, detail='Draft not found')
    draft.status = DraftStatus.approved
    draft.updated_at = datetime.utcnow()
    db.commit(); db.refresh(draft)
    return draft


@router.post('/drafts/{draft_id}/reject', response_model=DraftOut)
def reject_draft(draft_id: int, db: Session = Depends(get_db)):
    draft = db.get(Draft, draft_id)
    if not draft:
        raise HTTPException(status_code=404, detail='Draft not found')
    draft.status = DraftStatus.rejected
    draft.updated_at = datetime.utcnow()
    db.commit(); db.refresh(draft)
    return draft


@router.post('/drafts/{draft_id}/regenerate', response_model=DraftOut)
def regenerate_draft(draft_id: int, db: Session = Depends(get_db)):
    original = db.get(Draft, draft_id)
    if not original:
        raise HTTPException(status_code=404, detail='Draft not found')
    original.status = DraftStatus.rejected
    db.commit()
    return create_draft_from_trends(db, f'Regenerate based on {original.concept}')


@router.post('/drafts/{draft_id}/publish', response_model=DraftOut)
def publish_draft_route(draft_id: int, db: Session = Depends(get_db)):
    draft = db.get(Draft, draft_id)
    if not draft:
        raise HTTPException(status_code=404, detail='Draft not found')
    if draft.status not in [DraftStatus.approved, DraftStatus.draft]:
        raise HTTPException(status_code=400, detail='Draft must be approved or draft state')
    return publish_draft(db, draft)
