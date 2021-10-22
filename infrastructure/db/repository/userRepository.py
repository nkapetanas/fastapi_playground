from sqlalchemy.orm import Session

from business.users import User
from core.hashing import Hasher
from infrastructure.db.entities.users import User


def createNewUser(user: User, db: Session) -> User:
    user = User(username=user.username,
                email=user.email,
                hashed_password=Hasher.getHashedPassword(user.password),
                is_active=True,
                is_superuser=False)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
