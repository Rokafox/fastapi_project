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
    
def create_user(newuser_name: str, newuser_password: str, newuser_role: str):
    try:
        new_user = User(name=newuser_name, password=newuser_password, role=newuser_role)
    except Exception as e:
        return "Failed: " + str(e), False
    with Session(engine) as session:
        session.add(new_user)
        session.commit()
        return "User created successfully!", True
    
def create_project(newproject_name: str, newproject_description: str, 
                   newproject_starttime: str, newproject_endtime: str,
                   newproject_status: str):
    try:
        new_project = Project(name=newproject_name, description=newproject_description, 
                              starttime=newproject_starttime, endtime=newproject_endtime
                              , status=newproject_status)
    except Exception as e:
        return "Failed: " + str(e), False
    with Session(engine) as session:
        session.add(new_project)
        session.commit()
        return "Project created successfully!", True