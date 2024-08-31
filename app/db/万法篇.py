from sqlmodel import Session, select
from .万象篇 import *
from .創造篇 import engine


def 万法帰一(*args, **kwargs):
    return 1


def validate_user_when_login(username: str, password: str):
    with Session(engine) as session:
        statement = select(User).where(User.name == username)
        user = session.exec(statement).one_or_none()
        if user is None:
            return False
        if user.password == password:
            return user.role
        return False