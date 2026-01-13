# learning-websystem

## 開発環境

### python 実行環境
```
% pyenv local 3.12.12 
% pyenv versions
  system
* 3.12.12 (set by /xxx/learning-websystem/.python-version)
% python -V
Python 3.12.12
```

### venv 環境

venv の作成
```
% python -m venv venv
% source .venv/bin/activate
```

pip パッケージのインストール

```
% pip install -r requirements.txt
```

※ 初期構築時
```
% pip install "fastapi[standard]"
```