from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


class UserPublic(BaseModel):
    username: str
    email: EmailStr
    id: int

    # Função para transformar o json em um objeto python
    model_config = ConfigDict(from_attributes=True)


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserDB(UserSchema):
    id: int


class UserList(BaseModel):
    users: list[UserPublic]
