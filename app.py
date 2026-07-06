import uuid

from fastapi import FastAPI, Request, APIRouter, Form
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.sql import text
import datetime
import json
import hashlib
from pathlib import Path
from database_connecter import engine

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
        <p>只今、{now.strftime(f'%Y/%m/%d ({day_of_week}) %H:%M:%S')} です。</p>
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


@router.post("/web/user", response_class=HTMLResponse)
def create_user(request: Request, name: str = Form(...), email: str = Form(...), user_type: int = Form(...)):
    users_json_path = Path("files") / "users.json"
    with users_json_path.open("r", encoding="utf-8") as f:
        users_list = json.load(f)

    add_user = {
        "name": name,
        "email": email,
        "user_type": user_type
    }

    users_list.append(add_user)

    with users_json_path.open("w", encoding="utf-8") as f:
        json.dump(users_list, f, ensure_ascii=False, indent=4)

    response = templates.TemplateResponse(
        "user_created.html", {'request': request, 'user': add_user})
    return response


@router.get("/web/notifications", response_class=HTMLResponse)
def get_notifications(request: Request):
    notifications = []

    sql = """
          SELECT 
                 id,
                 notification_status,
                 title,
                 publication_start_date,
                 publication_end_date,
                 created_at
          FROM notifications
        """

    with engine.begin() as conn:
        rs = conn.execute(text(sql))

        if rs:
            notifications = [dict(row._mapping) for row in rs]

    response = templates.TemplateResponse(
        "notifications.html", {'request': request, 'notifications': notifications})
    return response

@router.get("/web2/notifications", response_class=HTMLResponse)
def get_notifications2(request: Request, title: str | None = None):
    notifications = []

    sql = """
          SELECT notification_status,
                 title,
                 publication_start_date,
                 publication_end_date,
                 created_at
          FROM notifications
        """

    if title:
        sql += f" WHERE title LIKE :title"

    with engine.begin() as conn:
        rs = conn.execute(text(sql), {'title': f'%{title}%'})

        if rs:
            notifications = [dict(row._mapping) for row in rs]

    response = templates.TemplateResponse(
        "notifications.html", {'request': request, 'notifications': notifications})
    return response


@router.get("/web/notification/{notification_id}", response_class=HTMLResponse)
def get_notifications(request: Request, notification_id: int):
    notification = {}

    sql = """
        SELECT 
            title,
            content_body,
            publication_start_date,
            publication_end_date,
            detail_image_path,
            link_url,
            created_at
        FROM notifications
        WHERE id = :notification_id
        """

    with engine.begin() as conn:
        rs = conn.execute(text(sql), {'notification_id': notification_id})

        row = rs.fetchone()
        if row:
            notification = dict( row._mapping)
        else:
            return templates.TemplateResponse("error_404.html", {'request': request}, status_code=404)

    response = templates.TemplateResponse(
        "notification_detail.html", {'request': request, 'notification': notification})
    return response


@router.get("/web/cookie", response_class=HTMLResponse)
def get_cookie(request: Request):

    last_access_datetime = "なし"
    if request.cookies.get('last_access_datetime'):
        last_access_datetime = request.cookies.get('last_access_datetime')

    html = f"""
            <html>
                <head>
                    <title>Cookie確認</title>
                </head>
                <body>
                    <p>前回アクセス日時 {last_access_datetime} </p>
                </body>
            </html>
            """
    response = HTMLResponse(content=html)

    now = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    response.set_cookie(key="last_access_datetime", value=now, max_age=60 * 10)

    return response

@router.get("/web/login", response_class=HTMLResponse)
def get_login(request: Request):
    response = templates.TemplateResponse("login.html", {'request': request})

    return response

@router.post("/web/login", response_class=HTMLResponse)
def post_login(
    request: Request,
    login_id: str = Form(...),
    login_password: str = Form(...),
):
    # リクエスト.login_passwordをハッシュ化
    hash_login_password = hashlib.sha256(login_password.encode()).hexdigest()

    # cms_usersテーブルから、login_id、login_password(ハッシュ値)で検索
    sql = """
          SELECT id,
                 user_name,
                 user_type
          FROM cms_users
          WHERE login_id = :login_id
            and login_password = :login_password \
          """

    with engine.begin() as conn:
        rs = conn.execute(text(sql), {'login_id': login_id, 'login_password': hash_login_password})
        row = rs.fetchone()

    if row:
        login_user = dict(row._mapping)
        response = templates.TemplateResponse("login_after.html",
                                              {'request': request,'login_user': login_user},
                                              status_code=200)
        # CookieにセッションIDを設定
        session_id = uuid.uuid4().hex
        session_valid_seconds = 60 * 15 # 15分
        response.set_cookie(key="session_id", value=session_id, max_age=session_valid_seconds)

        # DBにセッションIDを保管
        sql = """
        UPDATE cms_users SET session_id = :session_id WHERE id = :id
        """
        with engine.begin() as conn:
            conn.execute(text(sql), {'session_id': session_id, 'id': login_user['id']})

    else:
        response = templates.TemplateResponse("login.html",
                                          {
                                              'request': request,
                                              'error_message': 'ログインIDまたはパスワードが正しくありません'
                                          },
                                          status_code=200)

    return response


@router.get("/web/home", response_class=HTMLResponse)
def get_top(request: Request):

    # session_idからログインユーザを特定
    session_id = request.cookies.get('session_id')
    sql = """
          SELECT id,
                 user_name,
                 user_type
          FROM cms_users
          WHERE session_id = :session_id
          """

    with engine.begin() as conn:
        rs = conn.execute(text(sql), {'session_id': session_id})
        row = rs.fetchone()

    if row:
        login_user = dict(row._mapping)
        response = templates.TemplateResponse("home.html", {'request': request, 'login_user': login_user})
    else:
        response = RedirectResponse(url="/web/login")

    return response
app.include_router(router)