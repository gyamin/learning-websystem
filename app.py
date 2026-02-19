from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import datetime

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
    users_list = [
        {"name": "三浦", "email": "miura@local", "user_type": 1},
        {"name": "坂本", "email": "sakamoto@local", "user_type": 1},
        {"name": "高木", "email": "takagi@local", "user_type": 1},
        {"name": "高梨", "email": "takanashi@local", "user_type": 2},
        {"name": "木原", "email": "kihara@local", "user_type": 2},
    ]

    if name:
        response_list = [user for user in users_list if user['name'] == name]
    else:
        response_list = users_list

    return JSONResponse(response_list)

@router.get("/web/users", response_class=HTMLResponse)
def get_web_users(request: Request, name: str = None, response_class=HTMLResponse):
    users_list = [
        {"name": "三浦", "email": "miura@local", "user_type": 1},
        {"name": "坂本", "email": "sakamoto@local", "user_type": 1},
        {"name": "高木", "email": "takagi@local", "user_type": 1},
        {"name": "高梨", "email": "takanashi@local", "user_type": 2},
        {"name": "木原", "email": "kihara@local", "user_type": 2},
    ]

    if name:
        response_list = [user for user in users_list if user['name'] == name]
    else:
        response_list = users_list

    view_data = {'users': response_list}

    response = templates.TemplateResponse(
        "users.html", {'request': request, 'data': view_data})
    return response
app.include_router(router)