from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
import shutil
import time
from fastapi import Query
from .虚数篇 import *
from .指鹿篇 import 日本語になーれ
from .db.創造篇 import create_db_and_tables, create_sysadmin
from .db.万法篇 import *


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    code executed when the application starts and stops, before yield and after yield.
    If global_use_prev_db is True, do not create a new database, instead use the last modified database from ./old_db
    """
    if not os.path.exists("./old_db"):
        os.mkdir("./old_db")
    files = os.listdir("./old_db")
    files = [file for file in files if file.endswith(".db")]
    if global_use_prev_db and files:
        # get the most recent file from ./old_db
        files.sort(key=lambda x: os.path.getmtime(f"./old_db/{x}"))
        # move the most recent file to ./app/db/database.db
        shutil.move(f"./old_db/{files[-1]}", "./app/db/database.db")
    # else if database.db exists in ./app/db, do nothing
    elif os.path.exists("./app/db/database.db"):
        pass
    else:
        create_db_and_tables()
        create_sysadmin()
    # check if the database actually exists
    if not os.path.exists("./app/db/database.db"):
        print("WARNING: DATABASE NOT FOUND DURING STARTUP, APP WILL NOT FUNCTION!")
    yield
    # move the database from ./app/db/database.db to ./unrelated_files/old_db_{current_time}.db
    try:
        current_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        shutil.move("./app/db/database.db", f"./old_db/old_db_{current_time}.db")
    except FileNotFoundError:
        print("WARNING: DATABASE NOT FOUND DURING SHUTDOWN, NOT EXPECTED!")
        pass


app = FastAPI(lifespan=lifespan)


templates = Jinja2Templates(directory="app/templates")
if not os.path.exists("./app/static"):
    os.mkdir("./app/static")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

#英語
@app.get("/", response_class=HTMLResponse)
async def read_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

#日本語
@app.get("/login-jp", response_class=HTMLResponse)
async def read_login(request: Request):
    return templates.TemplateResponse("login-jp.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...), lang: str = Form("en")):
    user_role = validate_user_when_login(username, password)
    if user_role:
        template_name = "home.html" if lang == "en" else "home-jp.html"
        return templates.TemplateResponse(template_name, {"request": request, "username": username, "role": user_role, "password": password})
    else:
        template_name = "login.html" if lang == "en" else "login-jp.html"
        error_message = "Invalid credentials"
        if lang == "jp":
            error_message = 日本語になーれ(error_message)
        return templates.TemplateResponse(template_name, {"request": request, "error": error_message})

@app.post("/logout", response_class=HTMLResponse)
async def logout(request: Request, lang: str = Form("en")):
    template_name = "login.html" if lang == "en" else "login-jp.html"
    return templates.TemplateResponse(template_name, {"request": request})

# TODO: The below endpoints are extremely unsafe, anyone can access with simply like http://127.0.0.1:8000/home?username=doge&role=sysadmin
# 英語ページ
@app.get("/home", response_class=HTMLResponse)
async def home(request: Request, username: str, role: str, password: str):
    return templates.TemplateResponse("home.html", {"request": request, "username": username, "role": role, "password": password})

# 日本語ページ
@app.get("/home-jp", response_class=HTMLResponse)
async def home(request: Request, username: str, role: str, password: str):
    return templates.TemplateResponse("home-jp.html", {"request": request, "username": username, "role": role, "password": password})

# 日本語パスワード変更ページ
@app.get("/passwd-jp", response_class=HTMLResponse)
async def passwd_jp(request: Request, username: str, role: str, password: str):
    return templates.TemplateResponse("passwd-jp.html", {"request": request, "username": username, "role": role, "password": password})

# 英語パスワード
@app.get("/passwd", response_class=HTMLResponse)
async def passwd_en(request: Request, username: str, role: str, password: str):
    return templates.TemplateResponse("passwd.html", {"request": request, "username": username, "role": role, "password": password})

# 日本語ユーザ管理ページ
@app.get("/useradmin-jp", response_class=HTMLResponse)
async def useradmin_jp(request: Request, username: str, role: str, password: str):
    return templates.TemplateResponse("useradmin-jp.html", {"request": request, "username": username, "role": role, "password": password})

# 英語ユーザー管理ページ
@app.get("/useradmin", response_class=HTMLResponse)
async def useradmin(request: Request, username: str, role: str, password: str):
    return templates.TemplateResponse("useradmin.html", {"request": request, "username": username, "role": role, "password": password})

# 日本語プロジェクト管理ページ
@app.get("/project-jp", response_class=HTMLResponse)
async def project_jp(request: Request, username: str, role: str, password: str):
    return templates.TemplateResponse("project-jp.html", {"request": request, "username": username, "role": role, "password": password})

# 英語プロジェクト管理ページ
@app.get("/project-en", response_class=HTMLResponse)
async def project_en(request: Request, username: str, role: str, password: str):
    return templates.TemplateResponse("project-en.html", {"request": request, "username": username, "role": role, "password": password})

# 日本語ユーザ管理ページ
@app.get("/user-jp", response_class=HTMLResponse)
async def user_jp(request: Request, username: str, role: str, password: str):
    return templates.TemplateResponse("user-jp.html", {"request": request, "username": username, "role": role, "password": password})



# 英語task
@app.get("/task", response_class=HTMLResponse)
async def task(request: Request, username: str, role: str, password: str):
        return templates.TemplateResponse("task.html", {"request": request, "username": username, "role": role, "password": password})

# 日本語task
@app.get("/task-jp", response_class=HTMLResponse)
async def task_jp(request: Request, username: str, role: str, password: str):
    return templates.TemplateResponse("task-jp.html", {"request": request, "username": username, "role": role, "password": password})

# 英語プロジェクト割り当て
@app.get("/project-sub", response_class=HTMLResponse)
async def project_sub(request: Request, username: str, role: str, password: str):
        return templates.TemplateResponse("project-sub.html", {"request": request, "username": username, "role": role, "password": password})

# 日本語プロジェクト割り当て
@app.get("/project-sub-jp", response_class=HTMLResponse)
async def project_sub_jp(request: Request, username: str, role: str, password: str):
    return templates.TemplateResponse("project-sub-jp.html", {"request": request, "username": username, "role": role, "password": password})

# 英語出退
@app.get("/attendance", response_class=HTMLResponse)
async def attendance(request: Request, username: str, role: str, password: str):
        return templates.TemplateResponse("attendance.html", {"request": request, "username": username, "role": role, "password": password})

# 日本語出退
@app.get("/attendance-jp", response_class=HTMLResponse)
async def attendance_jp(request: Request, username: str, role: str, password: str):
    return templates.TemplateResponse("attendance-jp.html", {"request": request, "username": username, "role": role, "password": password})

# 英語ユーザー管理ページ
@app.get("/user", response_class=HTMLResponse)
async def user(request: Request, username: str, role: str, password: str):
        return templates.TemplateResponse("user.html", {"request": request, "username": username, "role": role, "password": password})

@app.post("/sysadmin_create_user", response_class=HTMLResponse)
async def sysadmin_create_user(request: Request, newuser_name: str = Form(...), 
                               newuser_password: str = Form(...), newuser_role: str = Form(...),
                               username: str = Form(...), role: str = Form(...), lang: str = Form("en"),
                               password: str = Form(...)):
    template_name = "useradmin.html" if lang == "en" else "useradmin-jp.html"
    if not validate_user_when_login(username, password):
        return templates.TemplateResponse("login.html", {"request": request})
    msg, successcheck = create_user(newuser_name, newuser_password, newuser_role)
    if lang == "jp":
        msg = 日本語になーれ(msg)
    return templates.TemplateResponse(template_name, {"request": request, "sysadmin_createuser_message": msg, 
                                                    "sysadmin_createuser_success": successcheck,
                                                    "username" : username, "role": role, "password": password})

@app.post("/sysadmin_delete_user", response_class=HTMLResponse)
async def sysadmin_delete_user(request: Request, deleteuser_name: str = Form(...), username: str = Form(...),
                               role: str = Form(...), lang: str = Form("en"), password: str = Form(...)):
    if not validate_user_when_login(username, password):
        return templates.TemplateResponse("login.html", {"request": request})
    # Make no sense to delete self
    if deleteuser_name == username:
        msg = "You cannot delete yourself!"
        successcheck = False
    else:
        msg, successcheck = order_delete_user_given_name(deleteuser_name)
    if lang == "jp":
        msg = 日本語になーれ(msg)
    template_name = "useradmin.html" if lang == "en" else "useradmin-jp.html"
    return templates.TemplateResponse(template_name, {"request": request, "sysadmin_deleteuser_message": msg,
                                                      "sysadmin_deleteuser_success": successcheck,
                                                      "username" : username, "role": role, "password": password})

@app.post("/genericuser_change_password", response_class=HTMLResponse)
async def genericuser_change_password(request: Request, newpassword: str = Form(...), username: str = Form(...),
                                        role: str = Form(...), lang: str = Form("en"), password: str = Form(...)):
    if not validate_user_when_login(username, password):
        return templates.TemplateResponse("login.html", {"request": request})
    msg, successcheck = order_change_password_given_name(username, newpassword)
    if lang == "jp":
        msg = 日本語になーれ(msg)
    template_name = "passwd.html" if lang == "en" else "passwd-jp.html"
    if not successcheck:
        newpassword = password
    return templates.TemplateResponse(template_name, {"request": request, "genericuser_changepassword_message": msg,
                                                    "genericuser_changepassword_success": successcheck,
                                                    "username" : username, "role": role, "password": newpassword})


@app.post("/sysadmin_create_project", response_class=HTMLResponse)
async def sysadmin_create_project(request: Request, newproject_name: str = Form(...), 
                                        newproject_description: str = Form(...),
                                        newproject_startdate: str = Form(...), 
                                        newproject_starttime: str = Form(...), 
                                        newproject_enddate: str = Form(...),
                                        newproject_endtime: str = Form(...),
                                        newproject_status: str = Form(...),
                                        project_manager_names: str = Form(...),  # 追加されたプロジェクトマネージャー名
                                        username: str = Form(...), role: str = Form(...), 
                                        lang: str = Form("en"), password: str = Form(...)):
    if not validate_user_when_login(username, password):
        return templates.TemplateResponse("login-jp.html", {"request": request})
    newproject_starttime = newproject_startdate + " " + newproject_starttime
    newproject_endtime = newproject_enddate + " " + newproject_endtime
    # プロジェクトマネージャー名をリストに変換（複数の名前がカンマで区切られている場合を想定）
    project_manager_name_list = [name.strip() for name in project_manager_names.split(",")]
    msg, successcheck = create_project(newproject_name, newproject_description, newproject_starttime, 
                                       newproject_endtime, newproject_status, project_manager_name_list)
    if lang == "jp":
        msg = 日本語になーれ(msg)
    template_name = "project.html" if lang == "en" else "project-jp.html"
    return templates.TemplateResponse(template_name, {
        "request": request, 
        "sysadmin_createproject_message": msg,
        "sysadmin_createproject_success": successcheck,
        "username": username, 
        "role": role, 
        "password": password
    })

@app.post("/sysadmin_retire_project_manager", response_class=HTMLResponse)
async def sysadmin_retire_project_manager(request: Request, retireproject_name: str = Form(...),
                                            retireprojectmanager_name: str = Form(...), username: str = Form(...),
                                            role: str = Form(...), lang: str = Form("en"), password: str = Form(...)):
        if not validate_user_when_login(username, password):
            return templates.TemplateResponse("login.html", {"request": request})
        msg, successcheck = order_retire_project_manager(retireprojectmanager_name, retireproject_name)
        if lang == "jp":
            msg = 日本語になーれ(msg)
        template_name = "project.html" if lang == "en" else "project-jp.html"
        return templates.TemplateResponse(template_name, {
            "request": request, 
            "sysadmin_retireprojectmanager_message": msg,
            "sysadmin_retireprojectmanager_success": successcheck,
            "username": username, 
            "role": role, 
            "password": password
        })

@app.post("/sysadmin_assign_project_manager", response_class=HTMLResponse)
async def sysadmin_assign_project_manager(request: Request, assignproject_name: str = Form(...),
                                            assignprojectmanager_name: str = Form(...), username: str = Form(...),
                                            role: str = Form(...), lang: str = Form("en"), password: str = Form(...)):
        if not validate_user_when_login(username, password):
            return templates.TemplateResponse("login.html", {"request": request})
        msg, successcheck = order_assign_project_manager(assignprojectmanager_name, assignproject_name)
        if lang == "jp":
            msg = 日本語になーれ(msg)
        template_name = "project.html" if lang == "en" else "project-jp.html"
        return templates.TemplateResponse(template_name, {
            "request": request, 
            "sysadmin_assignprojectmanager_message": msg,
            "sysadmin_assignprojectmanager_success": successcheck,
            "username": username, 
            "role": role, 
            "password": password
        })

@app.post("/pm_create_attendance", response_class=HTMLResponse)
async def pm_create_attendance(request: Request, pmasu_the_user_name: str = Form(...), pmasu_the_project_name: str = Form(...),
                               username: str = Form(...), role: str = Form(...), lang: str = Form("en"),
                               password: str = Form(...), selected_dates: list[str] = Form(...)):
    # print(selected_dates)
    # ['["2024-10-09","2024-10-10","2024-10-11","2024-10-14","2024-10-15","2024-10-16","2024-10-17"]']
    if not validate_user_when_login(username, password):
        return templates.TemplateResponse("login.html", {"request": request})
    msg, successcheck = create_attendance(pmasu_the_user_name, pmasu_the_project_name, date_list=selected_dates)
    if lang == "jp":
        msg = 日本語になーれ(msg)
    template_name = "project-sub.html" if lang == "en" else "project-sub-jp.html"
    return templates.TemplateResponse(template_name, {"request": request, "pm_createattendance_message": msg,
                                                    "pm_createattendance_success": successcheck,
                                                    "username" : username, "role": role, "password": password})

# pm delete attendance
@app.post("/pm_delete_attendance", response_class=HTMLResponse)
async def pm_delete_attendance(request: Request, pmuasu_the_user_name: str = Form(...), pmuasu_the_project_name: str = Form(...),
                               username: str = Form(...), role: str = Form(...), lang: str = Form("en"),
                               password: str = Form(...)):
    if not validate_user_when_login(username, password):
        return templates.TemplateResponse("login.html", {"request": request})
    msg, successcheck = order_delete_attendanc_given_name(pmuasu_the_user_name, pmuasu_the_project_name)
    if lang == "jp":
        msg = 日本語になーれ(msg)
    template_name = "project-sub.html" if lang == "en" else "project-sub-jp.html"
    return templates.TemplateResponse(template_name, {"request": request, "pm_deleteattendance_message": msg,
                                                    "pm_deleteattendance_success": successcheck,
                                                    "username" : username, "role": role, "password": password})

@app.post("/pm_create_task", response_class=HTMLResponse)
async def pm_create_task(request: Request, pmcreatetask_the_user_names: str = Form(...), pmcreatetask_the_project_name: str = Form(...),
                            the_task_status: str | None = Form(None), the_task_startdate: str = Form(...),
                            the_task_enddate: str = Form(...), username: str = Form(...), role: str = Form(...),
                            lang: str = Form("en"), password: str = Form(...)):
        if not validate_user_when_login(username, password):
            return templates.TemplateResponse("login.html", {"request": request})
        
        # user_names are comma separated, ie. "user1,user2,user3" ie. "doge"
        # we need to make it a list of user names
        user_names = [name.strip() for name in pmcreatetask_the_user_names.split(",")]
        msg, successcheck = order_create_task(user_names, pmcreatetask_the_project_name, the_task_startdate, the_task_enddate, the_task_status)
        if lang == "jp":
            msg = 日本語になーれ(msg)
    
        template_name = "task.html" if lang == "en" else "task-jp.html"
        return templates.TemplateResponse(template_name, {"request": request, "pm_createtask_message": msg,
                                                        "pm_createtask_success": successcheck,
                                                        "username" : username, "role": role, "password": password})



@app.get("/users")
async def read_users():
    return order_get_all_users()

@app.get("/users_hiruchaaru")
async def read_users_hiruchaaru():
    return order_get_all_hiruchaaru()


@app.patch("/users/{user_name}")
async def update_user(user_name: str, user: UserUpdate):
    msg, successcheck = order_update_user_by_id(user_name, user)
    return {"message": msg, "success": successcheck}

@app.get("/projects")
async def read_projects():
    return order_get_all_projects()

@app.get('/get_dates_from_project_name/{project_name}')
async def get_dates_from_project_name(project_name: str):
    something = order_get_dates_from_project_name(project_name)
    # print(something)
    return something

# project manager will only see the projects that they are managing
@app.get("/projects_pm/{project_manager_name}")
async def read_projects_by_project_manager(project_manager_name: str):
    return order_get_projects_by_project_manager(project_manager_name)

@app.delete("/projects/{project_id}")
async def delete_project(project_id: int):
    msg, successcheck = order_delete_project_by_id(project_id)
    return {"message": msg, "success": successcheck}

@app.patch("/projects/{project_id}")
async def update_project(project_id: int, project: ProjectUpdate):
    msg, successcheck = order_update_project_by_id(project_id, project)
    return {"message": msg, "success": successcheck}

@app.get("/attendances", response_model=list[AttendancePublic])
async def read_attendances():
    return order_get_all_attendances()

@app.get("/attendances/{user_name}")
async def read_attendances_by_user_name(user_name: str):
    return order_hiruchaaru_get_assigned_projects(user_name=user_name)

@app.post("/attendances/{attendance_id}/checkin")
async def checkin(attendance_id: int):
    msg, successcheck = order_hiruchaaru_checkin(attendance_id)
    return {"message": msg, "success": successcheck}

@app.post("/attendances/{attendance_id}/checkout")
async def checkout(attendance_id: int):
    msg, successcheck = order_hiruchaaru_checkout(attendance_id)
    return {"message": msg, "success": successcheck}

@app.get("/tasks", response_model=list[TaskPublic])
async def read_tasks():
    return order_get_all_tasks()

@app.get("/tasks_for_specific_hiruchaaru/{hiruchaaru_name}")
async def read_tasks_for_specific_hiruchaaru(hiruchaaru_name: str):
    return order_get_tasks_for_hiruchaaru(hiruchaaru_name)

@app.patch("/tasks/{task_id}")
async def update_task(task_id: int, task: TaskUpdate):
    msg, successcheck = order_update_task_by_id(task_id, task)
    return {"message": msg, "success": successcheck}

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    msg, successcheck = order_delete_task_by_id(task_id)
    return {"message": msg, "success": successcheck}