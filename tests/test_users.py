import json
import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.base import Base, get_db
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture
def delete_database():
    try:
        yield
    finally:
        os.remove("test.db")


def test_create_user():
    data = {
        "first_name": "Aleksandr",
        "last_name": "Ivanov",
        "patronymic": "Pavlovich",
        "email": "some_email@mail.ru",
        "password": "mypassword1",
    }
    response = client.post("/create", json=data)
    assert response.status_code == 200
    assert response.content == b'{"msg":"User with id 1 created"}'


def test_check_validate_email():
    data = {
        "first_name": "Aleksandr",
        "last_name": "Ivanov",
        "patronymic": "Pavlovich",
        "email": "some_email@mail.ru",
        "password": "mypassword1",
    }
    response = client.post("/create", json=data)
    assert response.status_code == 404
    assert response.content == b'{"detail":"email must be unique value"}'


def test_password_validate():
    data = {
        "first_name": "Aleksandr",
        "last_name": "Ivanov",
        "patronymic": "Pavlovich",
        "email": "some_email1@mail.ru",
        "password": "mypassword",
    }
    response = client.post("/create", json=data)
    assert response.status_code == 422
    assert response.reason == "Unprocessable Entity"


def test_email_validate():
    data = {
        "first_name": "Aleksandr",
        "last_name": "Ivanov",
        "patronymic": "Pavlovich",
        "email": "some_email1@mail.com",
        "password": "mypassword",
    }
    response = client.post("/create", json=data)
    assert response.status_code == 422
    assert response.reason == "Unprocessable Entity"


def test_update_user():
    data = {
        "first_name": "Nikolay",
        "last_name": "Ivanov",
        "patronymic": "Pavlovich",
        "email": "email1@mail.ru",
        "password": "mypassword2",
        "id": "1",
    }
    response = client.put("/update", json=data)
    assert response.status_code == 200
    assert response.content == b'{"msg":"The user with id 1 was modified"}'


def test_update_user_email_validation():
    data = {
        "first_name": "Nikolay",
        "last_name": "Ivanov",
        "patronymic": "Pavlovich",
        "email": "email_example@mail.ru",
        "password": "mypassword2",
    }
    response = client.post("/create", json=data)
    assert response.status_code == 200
    data = {
        "first_name": "Nikolay",
        "last_name": "Ivanov",
        "patronymic": "Pavlovich",
        "email": "email1@mail.ru",
        "password": "mypassword2",
        "id": 2,
    }
    response = client.put("/update", json=data)
    assert response.status_code == 409


def test_update_user_with_no_exist_id():
    data = {
        "first_name": "Nikolay",
        "last_name": "Ivanov",
        "patronymic": "Pavlovich",
        "email": "email1@mail.ru",
        "password": "mypassword2",
        "id": "1234",
    }
    response = client.put("/update", json=data)
    assert response.status_code == 404


def test_delete_user_with_no_exist_id():
    data = {"id": "1234"}
    response = client.delete("/delete", json=data)
    assert response.status_code == 404


def test_delete_user():
    data = {"id": "2"}
    response = client.delete("/delete", json=data)
    assert response.status_code == 200
    assert response.content == b'{"msg":"User with id 2 was deleted"}'


def test_get_user():
    response = client.get("/get_users/1")
    assert response.status_code == 200
    assert json.loads(response.content).get("first_name") == "Nikolay"


def test_get_user_with_no_exist_id():
    response = client.get("/get_users/1234")
    assert response.status_code == 404


def test_get_users():
    response = client.get("/get_users")
    assert response.status_code == 200


def test_get_user_by_field():
    response = client.get("/get_users_by_field?field=first_name&value=Nikolay")
    assert response.status_code == 200
    assert json.loads(response.content)[0].get("first_name") == "Nikolay"
    os.remove("test.db")
