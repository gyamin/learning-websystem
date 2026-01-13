from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import datetime

app = FastAPI()

router = APIRouter()

# テンプレートエンジン設定
templates = Jinja2Templates(directory="templates")

@router.get("/", tags=["webpage"], response_class=HTMLResponse)
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

@router.get("/greeting", tags=["webpage"], response_class=HTMLResponse)
def get_greeting(request: Request, name: str = "誰か"):
    greeting = f'こんにちは {name} さん'
    now = datetime.datetime.now()
    view_data = {'title': 'あいさつ', 'now': now.strftime(f'%Y/%m/%d %H:%M:%S'), 'greeting': greeting}
    response = templates.TemplateResponse(
        "greeting.html", {'request': request, 'data': view_data})
    return response

app.include_router(router)