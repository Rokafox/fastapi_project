from sqlmodel import Relationship, SQLModel, Field


class ProjectManagerAssign(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    project_id: int = Field(foreign_key="project.id", primary_key=True)


class UserBase(SQLModel):
    name: str = Field(unique=True)
    password: str = Field(min_length=4)
    role: str = Field(
        default="hiruchaaru",
        schema_extra={'pattern': '^(sysadmin|projectmanager|hiruchaaru)$'}
    )

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    attendances: list["Attendance"] = Relationship(back_populates="user", cascade_delete=True)
    managed_projects: list["Project"] = Relationship(
        back_populates="project_managers", link_model=ProjectManagerAssign
    )
    tasks: list["Task"] = Relationship(back_populates="user", cascade_delete=True)


class UserCreate(UserBase):
    pass

class UserPublic(UserBase):
    id: int

class UserUpdate(UserBase):
    name: str | None = None
    password: str | None = None
    role: str | None = None



class ProjectBase(SQLModel):
    name: str = Field(unique=True)
    description: str
    starttime: str
    endtime: str
    status: str = Field(
        default="scheduled",
        schema_extra={'pattern': '^(ongoing|completed|scheduled|failed|canceled|Requirements_Definition|Basic_Design|Detailed_Design|Programming|Unit_Testing|Integration_Testing|System_Testing)$'}
    )

class Project(ProjectBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    attendances: list["Attendance"] = Relationship(back_populates="project", cascade_delete=True)
    project_managers: list["User"] = Relationship(
        back_populates="managed_projects", link_model=ProjectManagerAssign
    )
    tasks: list["Task"] = Relationship(back_populates="project", cascade_delete=True)

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


class AttendanceBase(SQLModel):
    # Previous version
    # user_id: int | None = Field(default=None, foreign_key="user.id")
    # project_id: int | None = Field(default=None, foreign_key="project.id")
    user_id: int = Field(foreign_key="user.id")
    project_id: int = Field(foreign_key="project.id")
    date: str | None = Field(default=None)
    check_in: str | None = Field(default=None)
    check_out: str | None = Field(default=None)

class Attendance(AttendanceBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user: User | None = Relationship(back_populates="attendances")
    project: Project | None = Relationship(back_populates="attendances")

class AttendanceCreate(AttendanceBase):
    user_id: int
    project_id: int

class AttendancePublic(AttendanceBase):
    id: int
    user_id: int
    project_id: int
    # test
    user_name: str
    project_name: str
    project_starttime: str
    project_endtime: str


class TaskBase(SQLModel):
    user_id: int = Field(foreign_key="user.id")
    project_id: int = Field(foreign_key="project.id")
    start_date: str
    end_date: str
    status: str | None = Field(default=None)

class Task(TaskBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user: User | None = Relationship(back_populates="tasks")
    project: Project | None = Relationship(back_populates="tasks")

class TaskCreate(TaskBase):
    pass

class TaskPublic(TaskBase):
    id: int
    user_id: int
    user_name: str
    project_id: int
    project_name: str
    start_date: str
    end_date: str
    status: str | None

class TaskUpdate(TaskBase):
    user_id: int | None = None
    project_id: int | None = None
    start_date: str | None = None
    end_date: str | None = None
    status: str | None = None