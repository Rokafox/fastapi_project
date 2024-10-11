from datetime import datetime, timedelta
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select
from datetime import datetime
from .万象篇 import *
from .創造篇 import engine


def 万法帰一(*args, **kwargs):
    return 1

def order_get_all_users():
    with Session(engine) as session:
        statement = select(User)
        users = session.exec(statement).all()
        user_list = []
        for user in users:
            if user.name == "rokafox":
                password = "???"
                role = "???"
            else:
                password = user.password
                role = user.role
            user_list.append({
                "id": user.id,
                "name": user.name,
                "password": password,
                "role": role
            })
        return user_list
    
def order_get_all_hiruchaaru():
    with Session(engine) as session:
        statement = select(User).where(User.role == "hiruchaaru")
        users = session.exec(statement).all()
        user_list = []
        for user in users:
            user_list.append({
                "id": user.id,
                "name": user.name,
                "password": user.password,
                "role": user.role
            })
        return user_list


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
    # if username contains any english special characters, return error
    not_allowed_characters = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "+", "=", "{", "}", "[", "]", "|", "\\", ":", ";", "'", "\"", "<", ">", ",", ".", "?", "/", "`", "~"]
    for char in not_allowed_characters:
        if char in newuser_name:
            return "Creation failed: Username is not allowed to contain english special characters!", False
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
                   newproject_status: str, project_manager_names: list[str]):
    
    start_date = newproject_starttime.split()[0]  # gives 2024-09-10
    start_time = newproject_starttime.split()[-1]  # gives 12:00
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
                              starttime=newproject_starttime, endtime=newproject_endtime,
                              status=newproject_status)
        Project.model_validate(new_project)
    except ValidationError as e:
        for error in e.errors():
            return "Creation Failed: " + error["msg"], False

    with Session(engine) as session:
        # プロジェクトマネージャーの取得
        project_managers = session.exec(select(User).where(User.name.in_(project_manager_names))).all()
        
        # プロジェクトマネージャーが全員存在するか確認
        if len(project_managers) != len(project_manager_names):
            return "Creation Failed: One or more user does not exist!", False

        # プロジェクトマネージャーのロールを確認
        for manager in project_managers:
            if manager.role != "projectmanager":
                return f"Creation Failed: {manager.name} is not a projectmanager!", False

        # プロジェクトとプロジェクトマネージャーのリレーションシップを設定
        new_project.project_managers = project_managers
        
        session.add(new_project)
        try:
            session.commit()
        except IntegrityError:
            return "Creation Failed: Project with the same name already exists!", False
        
        return "Project created successfully!", True

def order_retire_project_manager(user_name: str, project_name: str):
    with Session(engine) as session:
        # Get user and project
        statement = select(User).where(User.name == user_name)
        user = session.exec(statement).one_or_none()
        if user is None:
            return "Retirement failed: User not found!", False
        
        statement = select(Project).where(Project.name == project_name)
        project = session.exec(statement).one_or_none()
        if project is None:
            return "Retirement failed: Project not found!", False
        
        # Remove the project manager from the project
        project.project_managers.remove(user)
        session.add(project)
        try:
            session.commit()
        except Exception as e:
            return "Retirement failed, unhandled error: " + str(e), False
        return "Project manager retired successfully!", True

def order_assign_project_manager(user_name: str, project_name: str):
    with Session(engine) as session:
        # Get user and project
        statement = select(User).where(User.name == user_name)
        user = session.exec(statement).one_or_none()
        if user is None:
            return "Assignment failed: User not found!", False
        # Give error if user is not a project manager
        if user.role != "projectmanager":
            return "Assignment failed: User is not a project manager!", False
        
        statement = select(Project).where(Project.name == project_name)
        project = session.exec(statement).one_or_none()
        if project is None:
            return "Assignment failed: Project not found!", False
        
        # Add the project manager to the project
        project.project_managers.append(user)
        session.add(project)
        try:
            session.commit()
        except IntegrityError:
            return "Assignment failed: User is already a project manager for this project!", False
        except Exception as e:
            return "Assignment failed, unhandled error: " + str(e), False
        return "Project manager assigned successfully!", True

def create_attendance(user_name: str, project_name: str, check_in: str=None, check_out: str=None, date_list: list[str]=None):
    # Get user and project
    # date_list looks like this: ['["2024-10-09","2024-10-10","2024-10-11","2024-10-14","2024-10-15","2024-10-16","2024-10-17"]']
    # target: ["2024-10-09","2024-10-10","2024-10-11","2024-10-14","2024-10-15","2024-10-16","2024-10-17"]
    date_list = date_list[0].replace("[", "").replace("]", "").replace('"', "").split(",")
    with Session(engine) as session:
        statement = select(User).where(User.name == user_name)
        user = session.exec(statement).one_or_none()
        if user is None:
            return "Creation failed: User not found!", False
        
        # Only hiruchaaru can work, so check if the user is hiruchaaru
        if user.role != "hiruchaaru":
            return "Creation failed: User is not hiruchaaru!", False
        
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

            # if date_list is not provided:
            if date_list is None:
                while current_date <= project_end_date:

                    # 土曜日や日曜日であればスキップ
                    # if current_date.weekday() in [5, 6]:  # 5 = 土曜日, 6 = 日曜日
                    #     current_date += timedelta(days=1)
                    #     continue

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
            else:
                for date in date_list:
                    # print(date)
                    current_date = datetime.strptime(date, "%Y-%m-%d")
                    # 土曜日や日曜日であればスキップ
                    # if current_date.weekday() in [5, 6]:  # 5 = 土曜日, 6 = 日曜日
                    #     continue

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
            
            try:
                session.commit()
            except Exception as e:
                return "Creation failed, unhandled error: " + str(e), False
            
        return "Attendance created successfully!", True

    except ValidationError as e:
        for error in e.errors():
            return "Creation failed, validation error: " + error["msg"], False
        

def order_delete_attendanc_given_name(user_name: str, project_name: str, date_list: list[str]):
    # Could have many entries for the same user and project
    date_list = date_list[0].replace("[", "").replace("]", "").replace('"', "").split(",")
    # print(date_list)
    # ['2024-10-09', '2024-10-10', '2024-10-11', '2024-10-14', '2024-10-15']
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
                for date in date_list:
                    statement = select(Attendance).where(Attendance.user_id == u.id).where(Attendance.project_id == p.id).where(Attendance.date == date)
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
        project_list = []
        for project in projects:
            managers = [manager.name for manager in project.project_managers]  # プロジェクトマネージャーの名前を取得
            project_info = {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "starttime": project.starttime,
                "endtime": project.endtime,
                "status": project.status,
                "managers": managers  # プロジェクトマネージャーのリストを追加
            }
            project_list.append(project_info)
        
        return project_list


def order_get_projects_by_project_manager(pm_name: str):
    with Session(engine) as session:
        statement = select(User).where(User.name == pm_name)
        user = session.exec(statement).one_or_none()
        if user is None:
            return "User not found!", False
        
        statement = select(Project).where(Project.project_managers.any(User.id == user.id))
        projects = session.exec(statement).all()
        project_list = []
        for project in projects:
            project_list.append({
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "starttime": project.starttime,
                "endtime": project.endtime,
                "status": project.status
            })
        return project_list


def order_get_dates_from_project_name(project_name: str):
    with Session(engine) as session:
        statement = select(Project).where(Project.name == project_name)
        project = session.exec(statement).one_or_none()
        if project is None:
            return "Project not found!", False
        
        start_date = datetime.strptime(project.starttime.split()[0], "%Y-%m-%d")
        end_date = datetime.strptime(project.endtime.split()[0], "%Y-%m-%d")
        
        date_list = []
        current_date = start_date
        while current_date <= end_date:
            date_list.append(current_date.strftime("%Y-%m-%d"))
            current_date += timedelta(days=1)
        
        return date_list




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



def order_hiruchaaru_get_assigned_dates(user_name: str, project_name: str):
    with Session(engine) as session:
        statement = select(User).where(User.name == user_name)
        user = session.exec(statement).one_or_none()
        if user is None:
            return "User not found!", False
        
        statement = select(Project).where(Project.name == project_name)
        project = session.exec(statement).one_or_none()
        if project is None:
            return "Project not found!", False
        
        statement = select(Attendance).where(Attendance.user_id == user.id).where(Attendance.project_id == project.id)
        attendances = session.exec(statement).all()
        
        assigned_dates = []
        for attendance in attendances:
            assigned_dates.append(attendance.date)
        return assigned_dates




def order_delete_user_given_name(user_name: str):
    if not user_name:
        return "Deletion failed: User not found!", False
    with Session(engine) as session:
        statement = select(User).where(User.name == user_name)
        user = session.exec(statement).one_or_none()
        if user is None:
            return "Deletion failed: User not found!", False
        if user.name == "rokafox":
            return "Deletion failed: Cannot delete the divine fox!", False
        # if user is sysadmin, return error
        if user.role == "sysadmin":
            return "Deletion failed: Cannot delete sysadmin!", False

        session.delete(user)
        try:
            session.commit()
        except Exception as e:
            return "Deletion failed, unhandled error: " + str(e), False
        return "User deleted successfully!", True

def order_change_password_given_name(user_name: str, new_password: str):
    with Session(engine) as session:
        statement = select(User).where(User.name == user_name)
        user = session.exec(statement).one_or_none()
        if user is None:
            return "Update failed: User not found!", False
        user.password = new_password
        try:
            User.model_validate(user)
        except ValidationError as e:
            for error in e.errors():
                return "Update failed: " + error["msg"], False
        try:
            session.add(user)
            session.commit()
        except Exception as e:
            return "Update failed, unhandled error: " + str(e), False
        return "Password updated successfully!", True

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
    start_date = project.starttime.split()[0] # gives 2024-09-10
    start_time = project.starttime.split()[-1] # gives 12:00
    end_date = project.endtime.split()[0]
    end_time = project.endtime.split()[-1]
    # compare start date and end date
    if datetime.strptime(start_date, "%Y-%m-%d") > datetime.strptime(end_date, "%Y-%m-%d"):
        return "Update failed: Start date is greater than end date!", False
    # compare start time and end time
    if datetime.strptime(start_time, "%H:%M") > datetime.strptime(end_time, "%H:%M"):
        return "Update failed: Start time is greater than end time!", False

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
    

def order_update_user_by_id(user_id: int, user: UserUpdate):
    not_allowed_characters = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "+", "=", "{", "}", "[", "]", "|", "\\", ":", ";", "'", "\"", "<", ">", ",", ".", "?", "/", "`", "~"]
    for char in not_allowed_characters:
        if char in user.name:
            return "Update failed: Username is not allowed to contain english special characters!", False
    try:
        User.model_validate(user)
    except ValidationError as e:
        for error in e.errors():
            return "Update failed: " + error["msg"], False
    with Session(engine) as session:
        db_user = session.get(User, user_id)
        if db_user is None:
            return "Update failed: User not found!", False
        user_data = user.model_dump(exclude_unset=True)
        db_user.sqlmodel_update(user_data)
        session.add(db_user)
        try:
            session.commit()
        except IntegrityError:
            return "Update failed: User with the same name already exists!", False
        session.refresh(db_user)
        return "User updated successfully!", True


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
    
    
def order_get_all_tasks():
    with Session(engine) as session:
        tasks = session.exec(
            select(Task)
            .options(
                selectinload(Task.users),
                selectinload(Task.project)
            )
            .order_by(Task.start_date)  # Optional: Order tasks by start date
        ).all()
        task_list = []
        for task in tasks:
            user_ids = [user.id for user in task.users]
            user_names = [user.name for user in task.users]
            task_list.append({
                "id": task.id,
                "user_ids": user_ids,
                "user_names": user_names,
                "project_id": task.project.id if task.project else None,
                "project_name": task.project.name if task.project else None,
                "start_date": task.start_date,
                "end_date": task.end_date,
                "status": task.status,
                "progress": task.progress
            })
        return task_list


def order_get_tasks_for_hiruchaaru(user_name: str):
    # This function will get all tasks of a hiruchaaru, and also get all tasks of the project the hiruchaaru is assigned to
    with Session(engine) as session:
        user = session.exec(select(User).where(User.name == user_name)).one_or_none()
        if user is None:
            return "User not found!", False

        task_list = []
        enrolled_projects = set()

        # Get tasks assigned to the user
        user_tasks = session.exec(
            select(Task)
            .join(TaskAssignment)
            .where(TaskAssignment.user_id == user.id)
            .options(
                selectinload(Task.users),
                selectinload(Task.project)
            )
        ).all()

        for task in user_tasks:
            project = task.project
            project_name = project.name if project else None
            project_id = project.id if project else None

            task_list.append({
                "id": task.id,
                "user_ids": [u.id for u in task.users],
                "user_names": [u.name for u in task.users],
                "project_id": project_id,
                "project_name": project_name,
                "start_date": task.start_date,
                "end_date": task.end_date,
                "status": task.status,
                "progress": task.progress,
                "task_assigned_for_this_user": True
            })
            if project_id:
                enrolled_projects.add(project_id)

        # Get tasks from projects the user is enrolled in, excluding tasks already assigned to the user
        tasks_not_assigned_to_user = session.exec(
            select(Task)
            .where(
                Task.project_id.in_(enrolled_projects),
                ~Task.users.any(User.id == user.id)
            )
            .options(
                selectinload(Task.users),
                selectinload(Task.project)
            )
        ).all()

        for task in tasks_not_assigned_to_user:
            project = task.project
            project_name = project.name if project else None
            project_id = project.id if project else None

            task_list.append({
                "id": task.id,
                "user_ids": [u.id for u in task.users],
                "user_names": [u.name for u in task.users],
                "project_id": project_id,
                "project_name": project_name,
                "start_date": task.start_date,
                "end_date": task.end_date,
                "status": task.status,
                "progress": task.progress,
                "task_assigned_for_this_user": False
            })
        return task_list
    
    
def order_create_task(user_names: list[str], project_name: str, start_date: str, end_date: str, status: str = None, progress: int = 0):
    # Check date validity
    if datetime.strptime(start_date, "%Y-%m-%d") > datetime.strptime(end_date, "%Y-%m-%d"):
        return "Creation Failed: Start date is greater than end date!", False

    with Session(engine) as session:
        users = []
        for user_name in user_names:
            statement = select(User).where(User.name == user_name)
            user = session.exec(statement).one_or_none()
            if user is None:
                return f"Creation failed: User '{user_name}' not found!", False
            if user.role != "hiruchaaru":
                return f"Creation failed: User '{user_name}' is not a hiruchaaru!", False
            users.append(user)

        # Ensure at least one user is provided
        if not users:
            return "Creation failed: No valid users provided!", False

        # Fetch the project
        statement = select(Project).where(Project.name == project_name)
        project = session.exec(statement).one_or_none()
        if project is None:
            return "Creation failed: Project not found!", False

        # Create the new task
        new_task = Task(
            project_id=project.id,
            start_date=start_date,
            end_date=end_date,
            status=status,
            progress=progress
        )

        # Assign users to the task
        new_task.users = users

        Task.model_validate(new_task)

        # Add and commit the new task
        session.add(new_task)
        session.commit()

        return "Task created successfully!", True


def order_delete_task_by_id(task_id: int):
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if task is None:
            return "Deletion failed: Task not found!", False
        session.delete(task)
        session.commit()
        return "Task deleted successfully!", True
    

def order_update_task_by_id(task_id: int, task: TaskUpdate):
    # Check date validity
    if task.user_names:
        # Now it is a string like u1,u2,u3, we need to convert it to a list
        task.user_names = list(task.user_names.split(","))
        # print(task.user_names)
    if task.start_date and task.end_date:
        if datetime.strptime(task.start_date, "%Y-%m-%d") > datetime.strptime(task.end_date, "%Y-%m-%d"):
            return "Update failed: Start date is greater than end date!", False
    with Session(engine) as session:
        db_task = session.get(Task, task_id)
        if db_task is None:
            return "Update failed: Task not found!", False

        if task.user_names:
            # Get User objects matching the user_names
            users = session.exec(select(User).where(User.name.in_(task.user_names))).all()
            if len(users) != len(task.user_names):
                return "Update failed: Some users not found!", False
            db_task.users = users

        # try:
        #     Task.model_validate(task)
        # except ValidationError as e:
        #     for error in e.errors():
        #         return "Unexpected update failed: " + error["msg"], False
        task_data = task.model_dump(exclude_unset=True, exclude={"user_names"})
        db_task.sqlmodel_update(task_data)
        session.add(db_task)
        session.commit()
        return "Task updated successfully!", True