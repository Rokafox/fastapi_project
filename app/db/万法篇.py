from datetime import datetime, timedelta
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select
from datetime import datetime
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
    
    start_date = newproject_starttime.split()[0] # gives 2024-09-10
    start_time = newproject_starttime.split()[-1] # gives 12:00
    end_date = newproject_endtime.split()[0]
    end_time = newproject_endtime.split()[-1]

    # compare start date and end date
    if datetime.strptime(start_date, "%Y-%m-%d") > datetime.strptime(end_date, "%Y-%m-%d"):
        return "Creation Failed: Start date is greater than end date!", False

    # compare start time and end time
    if datetime.strptime(start_time, "%H:%M") > datetime.strptime(end_time, "%H:%M"):
        return "Creation Failed: Start time is greater than end time!", False

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
    # If startdate is previous to today, set it to today
    if project_start_date < datetime.now():
        current_date = datetime.now()
    
    try:
        with Session(engine) as session:
            # get all attendances for this user and project, if there are any whose date is before than the project start date, delete them
            statement = select(Attendance).where(Attendance.user_id == user_id).where(Attendance.project_id == project_id)
            attendances = session.exec(statement).all()
            if attendances:
                for attendance in attendances:
                    if datetime.strptime(attendance.date, "%Y-%m-%d") < project_start_date:
                        session.delete(attendance)
                    # or if the date is after the project end date
                    elif datetime.strptime(attendance.date, "%Y-%m-%d") > project_end_date:
                        session.delete(attendance)
            else:
                pass

            while current_date <= project_end_date:
                # 既存の出席情報を確認
                existing_attendance = session.exec(
                    select(Attendance)
                    .where(Attendance.user_id == user_id)
                    .where(Attendance.project_id == project_id)
                    .where(Attendance.date == current_date.strftime("%Y-%m-%d"))
                ).one_or_none()

                if existing_attendance:
                    # return f"Creation failed: Same attendance already exists for {current_date.strftime('%Y-%m-%d')}", False
                    # instead of returning, we can just skip this date
                    current_date += timedelta(days=1)
                    continue

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
        

def order_delete_attendanc_given_name(user_name: str, project_name: str):
    # Could have many entries for the same user and project
    with Session(engine) as session:
        statement = select(User).where(User.name == user_name)
        user = session.exec(statement).all()
        if not user:
            return "Deletion failed: User not found!", False
        
        statement = select(Project).where(Project.name == project_name)
        project = session.exec(statement).all()
        if not project:
            return "Deletion failed: Project not found!", False
        
        for u in user:
            for p in project:
                statement = select(Attendance).where(Attendance.user_id == u.id).where(Attendance.project_id == p.id)
                attendance = session.exec(statement).all()
                if not attendance:
                    return "Deletion failed: Attendance not found!", False
                for a in attendance:
                    session.delete(a)
        try:
            session.commit()
        except Exception as e:
            return "Deletion failed, unhandled error: " + str(e), False
        return "Attendance deleted successfully!", True




def order_get_all_projects():
    with Session(engine) as session:
        statement = select(Project)
        projects = session.exec(statement).all()
        return projects

def order_hiruchaaru_get_assigned_projects(user_name: str):
    # Get records from attendances.
    # Get from User where name = user_name then get from attendances where user_id = user.id,
    # then get from attendances where date matches today's date, triple filter
    with Session(engine) as session:
        statement = select(User).where(User.name == user_name)
        user = session.exec(statement).one_or_none()
        if user is None:
            return "User not found!", False
        
        statement = select(Attendance).where(Attendance.user_id == user.id)
        attendances = session.exec(statement).all()

        today = datetime.now().strftime("%Y-%m-%d")
        attendances = [attendance for attendance in attendances if attendance.date.split()[0] == today]
        
        assigned_projects = []
        for attendance in attendances:
            assigned_projects.append({
                "id": attendance.id,
                "project_id": attendance.project_id,
                "project_name": attendance.project.name,
                "project_starttime": attendance.project.starttime.split(" ")[-1],
                "project_endtime": attendance.project.endtime.split(" ")[-1],
                "date": attendance.date,
                "check_in": attendance.check_in,
                "check_out": attendance.check_out,
            })
        return assigned_projects




def order_delete_user_given_name(user_name: str):
    with Session(engine) as session:
        statement = select(User).where(User.name == user_name)
        user = session.exec(statement).one_or_none()
        if user is None:
            return "Deletion failed: User not found!", False
        session.delete(user)
        try:
            session.commit()
        except Exception as e:
            return "Deletion failed, unhandled error: " + str(e), False
        return "User deleted successfully!", True

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
    

def order_hiruchaaru_checkin(attendance_id: int):
    with Session(engine) as session:
        attendance = session.get(Attendance, attendance_id)
        if attendance is None:
            return "Check-in failed: Attendance not found!", False
        attendance.check_in = datetime.now().strftime("%H:%M")
        session.add(attendance)
        session.commit()
        return "Check-in successful!", True
    
def order_hiruchaaru_checkout(attendance_id: int):
    with Session(engine) as session:
        attendance = session.get(Attendance, attendance_id)
        if attendance is None:
            return "Check-out failed: Attendance not found!", False
        attendance.check_out = datetime.now().strftime("%H:%M")
        session.add(attendance)
        session.commit()
        return "Check-out successful!", True