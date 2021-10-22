from pydantic import BaseModel, EmailStr


class UserJson(BaseModel):
    username: str
    email: EmailStr
    is_active: bool

    class Config():
        orm_mode = True
