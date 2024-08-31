from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
import shutil
import time
from .db.創造篇 import create_db_and_tables, create_sysadmin
from .db.万法篇 import validate_user_when_login


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    code executed when the application starts and stops, before yield and after yield
    """
    create_db_and_tables()
    create_sysadmin()
    # check if the database actually exists
    if not os.path.exists("./app/db/database.db"):
        print("WARNING: DATABASE NOT FOUND DURING STARTUP, APP WILL NOT FUNCTION!")
    yield
    # move the database from ./app/db/database.db to ./unrelated_files/old_db_{current_time}.db
    if not os.path.exists("./old_db"):
        os.mkdir("./old_db")
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