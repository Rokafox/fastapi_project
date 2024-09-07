from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    name: str = Field(unique=True)
    password: str = Field(min_length=4)
    role: str = Field(
        default="hiruchaaru",
        schema_extra={'pattern': '^(sysadmin|projectmanager|hiruchaaru)$'}
    )

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class UserCreate(UserBase):
    pass

class UserPublic(UserBase):
    id: int


class ProjectBase(SQLModel):
    name: str = Field(unique=True)
    description: str
    starttime: str
    endtime: str
    status: str = Field(
        default="scheduled",
        schema_extra={'pattern': '^(ongoing|completed|scheduled|failed|canceled)$'}
    )

class Project(ProjectBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class ProjectCreate(ProjectBase):
    pass

class ProjectPublic(ProjectBase):
    id: int

class ProjectUpdate(ProjectBase):
    name: str | None = None
    description: str | None = None
    starttime: str | None = None
    endtime: str | None = None
    status: str | None = None