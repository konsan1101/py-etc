#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://github.com/sky-joker/flask-login-example

from flask import Flask, request, Response, abort, render_template, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
import os

app = Flask(__name__, static_folder='templates/static')
app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password

# ログイン用ユーザー作成
users = {
    1: User(1, "1", "1"),
    2: User(2, "user", "pass")
}

# ユーザーチェックに使用する辞書作成
user_check = {}
for i in users.values():
    user_check[i.name] = {}
    user_check[i.name]['password'] = i.password
    user_check[i.name]['id'] = i.id

@login_manager.user_loader
def load_user(user_id):
    return users.get(int(user_id))

# ホーム
@app.route('/')
def home():
    return Response('''
    ホーム <br />
    <hr />
    <a href='/login/'>ログイン</a> <br />
    <a href='/menu/'>処理メニュー</a> <br />
    <a href='/logout/'>ログアウト</a> <br />
    ''')

# ログイン
@app.route('/login/', methods=["GET", "POST"])
def login():
    if(request.method == "GET"):
        return Response('''
            ログイン <br />
            <hr />
            <form action='' method='post'>
                <p><input type='text' name='username' id='username'>
                <p><input type='password' name='password' id='password'>
                <p><input type='submit' value='Login'>
            </form>
            ''')
    if(request.method == "POST"):
        username = request.form['username']
        password = request.form['password']
        # ユーザーチェック
        if(username in user_check):
            if (password == user_check[username]["password"]):
                # ユーザーが存在した場合はログイン
                login_user(users.get(user_check[username]["id"]))
                return Response('''
                login success! <br />
                <a href="/menu/">処理メニュー</a> <br />
                <a href="/logout/">ログアウト</a> <br />
                ''')
        return abort(401)

# 認証
@app.route('/auth/', methods=["GET", "POST"])
def auth():
        username = request.args.get('username')
        password = request.args.get('password')
        # ユーザーチェック
        if(username in user_check):
            if (password == user_check[username]["password"]):
                # ユーザーが存在した場合はログイン
                login_user(users.get(user_check[username]["id"]))
                return 'OK', 200
        return 'NG', 401

# 処理メニュー
@app.route('/menu/')
@login_required
def protected():
    return Response('''
    処理メニュー <br />
    <hr />
    None <br />
    <hr />
    <a href="/logout/">ログアウト</a> <br />
    ''')

# ログアウト
@app.route('/logout/', methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return Response('''
    logout success! <br />
    <a href="/">ホーム</a>
    ''')

# アイコン
@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, threaded=True, debug=True, )


