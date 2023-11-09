# twnlottobot
# 安裝django套件
- pip install django


# 建立專案
- django-admin startproject app-name

# 開啟目錄 

# 啟動Server
- python manage.py runserver


# 新增功能
- python manage.py startapp main

# git指令
1.安裝git
2.專案目錄底下

# 初始化本地倉庫  
- git init

# 產生忽略檔案
- .gitignore

# 檔案屬性
- U->UnTacked
- A->Added
- M->Modifed

# 加入控管
- git add <filename>
- git add .
	-  加入所有未控管/變動確認

# 確認儲存
- git commit -m "message" 

# 檢視狀態
- git status

# 檢視commit log 
- git log
	- git log --oneline

# 綁定遠端倉庫 
- git remote add origin https://github.com/YuYu0u0/twnlottobot
- git remote -v

# 複製專案
- git clone https://github.com/YuYu0u0/twnlottobot

# 同步資料庫
- python manage.py migrate

# 同步雲端倉庫 
- git push

# 啟動指令 
- gunicorn lotto.wsgi