from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True
