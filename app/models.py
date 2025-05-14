from pydantic import BaseModel

class User(BaseModel):
    email: str
    hashed_password: str
    role: str
    is_verified: bool = False
