from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.routers.user import get_current_user
from app.models.user import User
from app.services.recs import hybrid_recommendation

router = APIRouter()


@router.get("/")
def get_recommendations_ml(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    books = hybrid_recommendation(user.id, db)
    return books
