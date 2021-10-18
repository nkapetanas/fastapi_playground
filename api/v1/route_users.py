from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from infrastructure.db.repository.userRepository import createNewUser
from infrastructure.db.session import get_db
from schemas.users import UserCreate, ShowUser

router = APIRouter()


@router.post("/", response_model=ShowUser)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = createNewUser(user, db)
    return user
