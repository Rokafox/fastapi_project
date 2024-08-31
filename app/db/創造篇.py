from sqlmodel import Field, Session, SQLModel, create_engine, select
from .万象篇 import *


"""
TODO: We currently set echo=True, remove it in production
"""
engine = create_engine("sqlite:///./app/db/database.db", connect_args={"check_same_thread": False}, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def create_sysadmin():
    """
    We have to create enough sysadmins accounts
    """
    admin1 = User(name="doge", password="doge", role="sysadmin")
    admin2 = User(name="cate", password="cate", role="sysadmin")
    with Session(engine) as session:
        session.add(admin1)
        session.add(admin2)
        session.commit()