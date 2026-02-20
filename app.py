from fastapi import FastAPI, Request, APIRouter, Form
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import datetime
import json
from pathlib import Path


app = FastAPI()

router = APIRouter()

# テンプレートエンジン設定
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def get_root(request: Request):
    now = datetime.datetime.now()
    week_list = ["月", "火", "水", "木", "金", "土", "日"]
    day_of_week = week_list[now.weekday()]

    response = f"""
    <html>
    <head>
        <title>ルートページ</title>
    </head>
    <body>
        <p>只今、{ now.strftime(f'%Y/%m/%d ({day_of_week}) %H:%M:%S') } です。</p>
    </body>
    </html>
    """
    return response


@router.get("/greeting", response_class=HTMLResponse)
def get_greeting(request: Request, name: str = "誰か"):
    greeting = f'こんにちは {name} さん'
    now = datetime.datetime.now()
    view_data = {'title': 'あいさつ', 'now': now.strftime(f'%Y/%m/%d %H:%M:%S'), 'greeting': greeting}
    response = templates.TemplateResponse(
        "greeting.html", {'request': request, 'data': view_data})
    return response


@router.get("/api/users", response_class=JSONResponse)
def get_api_users(request: Request, name: str = None):
    # users.json からuser一覧を取得
    users_json_path = Path("files") / "users.json"

    with users_json_path.open("r", encoding="utf-8") as f:
        users_list = json.load(f)

    if name:
        response_list = [user for user in users_list if user['name'] == name]
    else:
        response_list = users_list

    return JSONResponse(response_list)

@router.get("/web/users", response_class=HTMLResponse)
def get_web_users(request: Request, name: str = None):
    # users.json からuser一覧を取得
    users_json_path = Path("files") / "users.json"

    with users_json_path.open("r", encoding="utf-8") as f:
        users_list = json.load(f)

    if name:
        response_list = [user for user in users_list if user['name'] == name]
    else:
        response_list = users_list

    view_data = {'users': response_list}

    response = templates.TemplateResponse(
        "users.html", {'request': request, 'data': view_data})
    return response


@router.get("/web/user/new", response_class=HTMLResponse)
def get_user_new(request: Request):

    response = templates.TemplateResponse(
        "user_new.html", {'request': request})
    return response


@router.post("/web/user", response_class=RedirectResponse)
def create_user(name: str = Form(...), email: str = Form(...), user_type: int = Form(...)):
    users_json_path = Path("files") / "users.json"
    with users_json_path.open("r", encoding="utf-8") as f:
        users_list = json.load(f)

    users_list.append({
        "name": name,
        "email": email,
        "user_type": user_type
    })

    with users_json_path.open("w", encoding="utf-8") as f:
        json.dump(users_list, f, ensure_ascii=False, indent=4)

    return RedirectResponse(url="/web/users", status_code=303)
app.include_router(router)