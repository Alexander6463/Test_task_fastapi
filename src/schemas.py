from typing import Optional, List

from pydantic import BaseModel, validator, Field
from validate_email import validate_email


class User(BaseModel):
    first_name: str = Field(example="Alexander")
    last_name: str = Field(example="Ivanov")
    patronymic: Optional[str] = Field(example="Pavlovich")
    email: Optional[str] = Field(example="example@mail.com")
    password: str = Field(example="mypassword1")

    @validator("password")
    def validate_password(cls, password):
        print(password)
        if (
            not password.isalnum()
            or password.isalpha()
            or password.isnumeric()
            or len(password) < 6
        ):
            raise ValueError("password error")
        return password

    @validator("email")
    def validate_email(cls, email):
        if not validate_email(email):
            raise ValueError("email error")
        return email


class UserFind(BaseModel):
    field: str = Field(example="first_name, last_name, patronymic, email")
    value: str = Field(example="Alexandr")

    @validator("field")
    def validate_field_value(cls, field):
        if field not in {"first_name", "last_name", "patronymic", "email"}:
            return False
        return field


class Users(BaseModel):
    users: List[User]


class UserUpdate(User):
    id: str = Field(example="1")


class UserUpdateWrongResponse(BaseModel):
    detail: str = Field(example="User with such email already exist")


class UserId(BaseModel):
    id: str = Field(example="1")


class UserCreateResponse(BaseModel):
    msg: str = Field(example="User with id 1 created")


class UserCreateWrongResponse(BaseModel):
    detail: str = Field(example="email must be unique")


class UserDeleteResponse(BaseModel):
    msg: str = Field(example="User with id 1 deleted")


class UserWrongResponse(BaseModel):
    detail: str = Field(example="User is not exist")


class UsersWrongResponse(BaseModel):
    detail: str = Field(example="Users are not exist")


class FieldWrongResponse(BaseModel):
    detail: str = Field(example="Enter correct field")
