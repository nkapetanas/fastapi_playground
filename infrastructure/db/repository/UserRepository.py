from sqlalchemy.orm import Session

from business.users import User
from core.hashing import Hasher
from infrastructure.db.entities.UserEntity import UserEntity


def createNewUser(user: User, db: Session) -> UserEntity:
    user = UserEntity(username=user.username,
                      email=user.email,
                      hashed_password=Hasher.getHashedPassword(user.password),
                      is_active=True,
                      is_superuser=False)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
