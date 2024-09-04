from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    password: str = Field(min_length=5)
    # role only allows 3 values: "sysadmin", "projectmanager", "hiruchaaru"
    role: str = Field(
        default="hiruchaaru",
        regex="^(sysadmin|projectmanager|hiruchaaru)$"
    )

class Project(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str
    starttime: str
    endtime: str
    status: str = Field(
        default="scheduled",
        regex="^(ongoing|completed|scheduled|failed|canceled)$"
    )
