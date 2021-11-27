import datetime

from fastapi import APIRouter, Depends, HTTPException
import logging
from db import models
from db.base import get_db
from src.schemas import (
    User,
    Users,
    UserUpdate,
    UserId,
    UserCreateResponse,
    UserCreateWrongResponse,
    UserDeleteResponse,
    UserWrongResponse,
    UserUpdateWrongResponse,
    UserFind,
    FieldWrongResponse,
)
from src.security import get_password_hash
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import and_


router = APIRouter()


LOGGER = logging.getLogger(name="model_ui")


@router.post(
    "/create",
    responses={
        200: {
            "model": UserCreateResponse,
            "description": "Successfully created",
        },
        404: {
            "model": UserCreateWrongResponse,
            "description": "email must be unique value",
        },
    },
)
def create_user(request: User, session: Session = Depends(get_db)):
    if (
        session.query(models.User)
        .filter(models.User.email == request.email)
        .all()
    ):
        LOGGER.info(
            "Create user get already existing user email %s",
            request.email,
        )
        raise HTTPException(
            status_code=404, detail="email must be unique value"
        )
    LOGGER.info("Creating new user")
    new_user = models.User(
        first_name=request.first_name,
        last_name=request.last_name,
        patronymic=request.patronymic,
        email=request.email,
        password=get_password_hash(request.password),
        date_created=datetime.datetime.now(),
    )
    session.add(new_user)
    session.commit()
    return {"msg": f"User with id {new_user.id} created"}


@router.put(
    "/update",
    responses={
        200: {
            "model": UserCreateResponse,
            "description": "Successfully created",
        },
        404: {
            "model": UserCreateWrongResponse,
            "description": "user with such id is not exist",
        },
        409: {
            "model": UserUpdateWrongResponse,
            "description": "user with such email already exist",
        },
    },
)
def update_user(request: UserUpdate, session: Session = Depends(get_db)):
    user = session.query(models.User).get(request.id)
    if not user:
        LOGGER.info("User with such id %s is not exist", request.id)
        raise HTTPException(
            status_code=404, detail="User with such id is not exist"
        )
    if (
        session.query(models.User)
        .filter(
            and_(
                models.User.email == request.email,
                models.User.id != request.id,
            )
        )
        .all()
    ):
        LOGGER.info("User with such email %s already exist", request.email)
        raise HTTPException(
            status_code=409,
            detail="User with such email already exist",
        )
    LOGGER.info("Update user with id %s", request.id)
    user.first_name = request.first_name
    user.last_name = request.last_name
    user.email = request.email
    user.password = get_password_hash(request.password)
    user.updated = datetime.datetime.now()
    session.commit()
    return {"msg": f"The user with id {request.id} was modified"}


@router.delete(
    "/delete",
    responses={
        200: {
            "model": UserDeleteResponse,
            "description": "Successfully deleted",
        },
        404: {
            "model": UserWrongResponse,
            "description": "User id error",
        },
    },
)
def delete_user(request: UserId, session: Session = Depends(get_db)):
    user = session.query(models.User).get(request.id)
    if not user:
        LOGGER.info("User with such id %s is not exist", request.id)
        raise HTTPException(
            status_code=404, detail="User with such id is not exist"
        )
    session.delete(user)
    session.commit()
    LOGGER.info("User with id %s was deleted", request.id)
    return {"msg": f"User with id {request.id} was deleted"}


@router.get(
    "/get_users/{user_id}",
    responses={
        200: {
            "model": User,
            "description": "Successful",
        },
        404: {
            "model": UserWrongResponse,
            "description": "User id error",
        },
    },
)
def get_users(user_id: int, session: Session = Depends(get_db)):
    try:
        user = (
            session.query(models.User).filter(models.User.id == user_id).one()
        )
    except NoResultFound:
        LOGGER.error("Get user by id get not existing id %s", user_id)
        raise HTTPException(status_code=404, detail="Not existing user id")
    return user


@router.get(
    "/get_users",
    responses={
        200: {
            "model": Users,
            "description": "Successful",
        },
        404: {
            "model": UserWrongResponse,
            "description": "Users are not exist",
        },
    },
)
def get_users(session: Session = Depends(get_db)):
    try:
        users = session.query(models.User).all()
    except NoResultFound:
        LOGGER.error("Users are not exist")
        raise HTTPException(status_code=404, detail="Users are not exist")
    return users


@router.get(
    "/get_users_by_field",
    responses={
        200: {
            "model": Users,
            "description": "Successful",
        },
        404: {
            "model": FieldWrongResponse,
            "description": "Enter correct field",
        },
    },
)
def get_users_filter(
    request: UserFind = Depends(), session: Session = Depends(get_db)
):
    if not request.field:
        raise HTTPException(status_code=404, detail="Enter correct field")
    if request.field == "first_name":
        return (
            session.query(models.User)
            .filter(models.User.first_name == request.value)
            .all()
        )
    elif request.field == "last_name":
        return (
            session.query(models.User)
            .filter(models.User.last_name == request.value)
            .all()
        )
    elif request.field == "email":
        return (
            session.query(models.User)
            .filter(models.User.email == request.value)
            .all()
        )
    return (
        session.query(models.User)
        .filter(models.User.patronymic == request.value)
        .all()
    )
