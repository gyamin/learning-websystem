FROM python:3.12
WORKDIR /code

# pip パッケージインストール
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# アプリケーション関連ファイルをコピー
COPY ./app.py /code/
COPY ./database_connecter.py /code/
COPY ./.env.docker /code/.env
COPY ./files /code/files/
COPY ./templates /code/templates/

# アプリケーション起動
CMD ["fastapi", "run", "app.py", "--port", "8000"]