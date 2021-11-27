from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])


def get_password_hash(password: str):
    return pwd_context.hash(password)
