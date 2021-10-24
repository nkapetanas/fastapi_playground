from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.v1.users.UserJson import UserJson
from infrastructure.db.repository.UserRepository import createNewUser
from infrastructure.db.session import get_db
from business.users import User

router = APIRouter()


@router.post("/", response_model=UserJson)
def create_user(user: User, db: Session = Depends(get_db)):
    user = createNewUser(user, db)
    return user
