from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    password: str
    # role only allows 3 values: "sysadmin", "projectmanager", "hiruchaaru"
    role: str = Field(
        default="hiruchaaru",
        regex="^(sysadmin|projectmanager|hiruchaaru)$"
    )

