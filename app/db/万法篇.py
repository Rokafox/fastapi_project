from datetime import datetime, timedelta
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
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
        User.model_validate(new_user)
    except ValidationError as e:
        for error in e.errors():
            return "Creation failed: " + error["msg"], False
    with Session(engine) as session:
        session.add(new_user)
        try:
            session.commit()
        except IntegrityError:
            return "Creation failed: User with the same name already exists!", False
        return "User created successfully!", True
    
def create_project(newproject_name: str, newproject_description: str, 
                   newproject_starttime: str, newproject_endtime: str,
                   newproject_status: str):
    try:
        new_project = Project(name=newproject_name, description=newproject_description, 
                              starttime=newproject_starttime, endtime=newproject_endtime
                              , status=newproject_status)
        Project.model_validate(new_project)
    except ValidationError as e:
        for error in e.errors():
            return "Creation Failed: " + error["msg"], False
    with Session(engine) as session:
        session.add(new_project)
        try:
            session.commit()
        except IntegrityError:
            return "Creation Failed: Project with the same name already exists!", False
        return "Project created successfully!", True
    

def create_attendance(user_name: str, project_name: str, check_in: str=None, check_out: str=None):
    # Get user and project
    with Session(engine) as session:
        statement = select(User).where(User.name == user_name)
        user = session.exec(statement).one_or_none()
        if user is None:
            return "Creation failed: User not found!", False
        
        statement = select(Project).where(Project.name == project_name)
        project = session.exec(statement).one_or_none()
        if project is None:
            return "Creation failed: Project not found!", False
    
    user_id = user.id
    project_id = project.id
    
    # プロジェクトの開始日と終了日を取得
    project_start_date = datetime.strptime(project.starttime.split()[0], "%Y-%m-%d")
    project_end_date = datetime.strptime(project.endtime.split()[0], "%Y-%m-%d")
    
    # 開始日から終了日までの日数を計算
    current_date = project_start_date
    
    # 出席情報を各日付ごとに作成
    try:
        with Session(engine) as session:
            while current_date <= project_end_date:
                # 既存の出席情報を確認
                existing_attendance = session.exec(
                    select(Attendance)
                    .where(Attendance.user_id == user_id)
                    .where(Attendance.project_id == project_id)
                    .where(Attendance.date == current_date.strftime("%Y-%m-%d"))
                ).one_or_none()

                if existing_attendance:
                    return f"Creation failed: Same attendance already exists for {current_date.strftime('%Y-%m-%d')}", False

                # 新しい出席情報を作成
                new_attendance = Attendance(
                    user_id=user_id,
                    project_id=project_id,
                    date=current_date.strftime("%Y-%m-%d"),
                    check_in=check_in,
                    check_out=check_out
                )
                Attendance.model_validate(new_attendance)
                session.add(new_attendance)
                current_date += timedelta(days=1)
            
            try:
                session.commit()
            except Exception as e:
                return "Creation failed, unhandled error: " + str(e), False
            
        return "Attendance created successfully!", True

    except ValidationError as e:
        for error in e.errors():
            return "Creation failed, validation error: " + error["msg"], False
        

def order_get_all_projects():
    with Session(engine) as session:
        statement = select(Project)
        projects = session.exec(statement).all()
        return projects
    
def order_get_projects_with_limit(limit: int = 100, offset: int = 100):
    with Session(engine) as session:
        statement = select(Project).limit(limit).offset(offset)
        projects = session.exec(statement).all()
        return projects
    
def order_delete_project_by_its_name(project_name: str):
    with Session(engine) as session:
        statement = select(Project).where(Project.name == project_name)
        project = session.exec(statement).one_or_none()
        if project is None:
            return "Deletion failed: Project not found!", False
        session.delete(project)
        session.commit()
        return "Project deleted successfully!", True
    
def order_delete_project_by_id(project_id: int):
    with Session(engine) as session:
        statement = select(Project).where(Project.id == project_id)
        project = session.exec(statement).one_or_none()
        if project is None:
            return "Deletion failed: Project not found!", False
        session.delete(project)
        session.commit()
        return "Project deleted successfully!", True
    
def order_update_project_by_id(project_id: int, project: ProjectUpdate):
    with Session(engine) as session:
        db_project = session.get(Project, project_id)
        if db_project is None:
            return "Update failed: Project not found!", False
        project_data = project.model_dump(exclude_unset=True)
        db_project.sqlmodel_update(project_data)
        session.add(db_project)
        try:
            session.commit()
        except IntegrityError:
            return "Update failed: Project with the same name already exists!", False
        session.refresh(db_project)
        return "Project updated successfully!", True
    
    
def order_get_all_attendances():
    with Session(engine) as session:
        # Attendanceと関連するUser、Projectを取得する
        statement = select(Attendance, User.name, Project.name).join(Attendance.user).join(Attendance.project)
        results = session.exec(statement).all()
        
        attendances_with_details = []
        for attendance, user_name, project_name in results:
            attendances_with_details.append({
                "id": attendance.id,
                "user_id": attendance.user_id,
                "user_name": user_name,
                "project_id": attendance.project_id,
                "project_name": project_name,
                "project_starttime": attendance.project.starttime.split(" ")[-1],
                "project_endtime": attendance.project.endtime.split(" ")[-1],
                "date": attendance.date,
                "check_in": attendance.check_in,
                "check_out": attendance.check_out,
            })
        return attendances_with_details