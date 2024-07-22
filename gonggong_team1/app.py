from flask import Flask, render_template, session, request, url_for, redirect, send_file, abort
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
import hashlib
import sqlite3
import secrets
import os

app = Flask(__name__)
# 키값 설정
app.secret_key = secrets.token_hex(256)
# 세션 타임 설정
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=60)
# 세션 타입 설정
app.config['SESSION_TYPE'] = 'filesystem'

# 비밀번호 암호화
def password_sha_512_hash(data):
    # 데이터를 UTF-8 인코딩으로 변환하여 해싱합니다.
    encoded_data = data.encode('utf-8')
    hashed_data = hashlib.sha512(encoded_data).hexdigest()
    return hashed_data

# DB 연동
db_path = "main.db"
conn = sqlite3.connect(db_path, check_same_thread=False)
cur = conn.cursor() 

# 메인 페이지
@app.route('/')
def home():
    return render_template('main.html')

# 회사 소개
@app.route('/e_intro', methods=['GET', 'POST'])
def e_intro():
    return render_template('e_intro.html', title='기업 소개')

# 사업 소개
@app.route('/b_intro', methods=['GET', 'POST'])
def b_intro():
    return render_template('b_intro.html', title='사업 소개')

# 서비스1
@app.route('/serv1', methods=['GET', 'POST'])
def serv1():
    return render_template('serv1.html', title='서비스1')

# 서비스2
@app.route('/serv2', methods=['GET', 'POST'])
def serv2():
    return render_template('serv2.html', title='서비스2')

# 서비스 3
@app.route('/serv3', methods=['GET', 'POST'])
def serv3():
    return render_template('serv3.html', title='서비스3')

# 회원가입
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        try:
            id = request.form['id']
            name = request.form['name']
            username = request.form['username']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            email = request.form['email']
            phone_number = request.form['phone_number']
            authority = 0
            status = 1
            if password == confirm_password:
                password = password_sha_512_hash(password)
                insert_query = """
                INSERT INTO user (id, username, name, pw, email, phone, authority, status) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """
                cur.execute(insert_query, (id, username, name, password, email, phone_number, authority, status))
                conn.commit()
                return render_template('login.html')
        except sqlite3.IntegrityError:
            msg = "회원가입 실패"
            return render_template('register.html', msg=msg)

# 로그인
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        try:
            id = request.form['id']
            password = request.form['password']
            password = password_sha_512_hash(password)
            select_query = """
            SELECT id, username, authority FROM user WHERE id = ? AND pw = ?
            """
            cur.execute(select_query, (id, password))
            user = cur.fetchone()
            select_query = """
            SELECT COUNT(*) FROM login_logs WHERE u_id = ? AND rdate > DATETIME('now', '-30 minute') 
            """
            cur.execute(select_query, (id, ))
            login_logs_count = cur.fetchone()
            if login_logs_count[0] >= 5 :
                msg = "5회 이상 틀렸습니다. 30분 뒤에 다시 시도 해주세요!"
                return render_template('login.html', msg=msg)
            if user is None:
                insert_query = """
                INSERT INTO login_logs (u_id) 
                VALUES (?)
                """
                cur.execute(insert_query, (id))
                conn.commit()
                return render_template('login.html')
            session['id'] = user[0]
            session['username'] = user[1]
            session['authority'] = user[2]
            return render_template('main.html')
        except sqlite3.IntegrityError:
            msg = "로그인 실패"
            return render_template('login.html', msg=msg)

# 나의 정보 페이지
@app.route('/mypage', methods=['GET', 'POST'])
def mypage():
    return render_template('mypage.html', title='나의 페이지')

# 로그아웃
@app.route('/logout', methods=['GET'])
def logout():
    if request.method == 'GET':
        session.clear()
        return render_template('main.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=8000, debug=True)
