from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
import shutil
import time
from .虚数篇 import *
from .db.創造篇 import create_db_and_tables, create_sysadmin
from .db.万法篇 import validate_user_when_login, create_user, create_project


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    code executed when the application starts and stops, before yield and after yield.
    If global_use_prev_db is True, do not create a new database, instead use the last modified database from ./old_db
    """
    if not os.path.exists("./app/static"):
        os.mkdir("./app/static")
    if not os.path.exists("./old_db"):
        os.mkdir("./old_db")
    files = os.listdir("./old_db")
    files = [file for file in files if file.endswith(".db")]
    if global_use_prev_db and files:
        # get the most recent file from ./old_db
        files.sort(key=lambda x: os.path.getmtime(f"./old_db/{x}"))
        # move the most recent file to ./app/db/database.db
        shutil.move(f"./old_db/{files[-1]}", "./app/db/database.db")
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
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user_role = validate_user_when_login(username, password)
    if user_role:
        return templates.TemplateResponse("home.html", {"request": request, "username": username, "role": user_role})
    else:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

@app.post("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/sysadmin_create_user", response_class=HTMLResponse)
async def sysadmin_create_user(request: Request, newuser_name: str = Form(...), 
                               newuser_password: str = Form(...), newuser_role: str = Form(...),
                               username: str = Form(...), role: str = Form(...)):
    msg, successcheck = create_user(newuser_name, newuser_password, newuser_role)
    return templates.TemplateResponse("home.html", {"request": request, "sysadmin_createuser_message": msg, 
                                                    "sysadmin_createuser_success": successcheck,
                                                    "username" : username, "role": role})

@app.post("/sysadmin_create_project", response_class=HTMLResponse)
async def sysadmin_create_project(request: Request, newproject_name: str = Form(...), 
                                        newproject_description: str = Form(...),
                                        newproject_startdate: str = Form(...), 
                                        newproject_starttime: str = Form(...), 
                                        newproject_enddate: str = Form(...),
                                        newproject_endtime: str = Form(...),
                                        newproject_status: str = Form(...),
                                        username: str = Form(...), role: str = Form(...)):
    newproject_starttime = newproject_startdate + " " + newproject_starttime
    newproject_endtime = newproject_enddate + " " + newproject_endtime
    msg, successcheck = create_project(newproject_name, newproject_description, newproject_starttime, 
                         newproject_endtime, newproject_status)
    return templates.TemplateResponse("home.html", {"request": request, "sysadmin_createproject_message": msg,
                                                    "sysadmin_createproject_success": successcheck,
                                                    "username" : username, "role": role})