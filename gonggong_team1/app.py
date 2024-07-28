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
cur.execute('''
CREATE TABLE IF NOT EXISTS user (
    username VARCHAR(20) PRIMARY KEY,
    name VARCHAR(20),
    gender VARCHAR(20),
    birthdate DATETIME,
    password VARCHAR(20),
    confirm_password VARCHAR(20),
    phone VARCHAR(20),
    address VARCHAR(256),
    email VARCHAR(128),
    diseases VARCHAR(128),
    medications VARCHAR(128)
)
''')
cur.execute('''
CREATE TABLE IF NOT EXISTS login_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    u_id TEXT NOT NULL,
    rdate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(u_id) REFERENCES user(id)
)
''')
conn.commit()

# 메인 페이지
@app.route('/')
def home():
    msg = request.args.get('msg')
    return render_template('main.html', msg=msg)

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
# 서비스 4
@app.route('/serv4', methods=['GET', 'POST'])
def serv4():
    return render_template('serv4.html', title='서비스4')

# 회원가입
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            name = request.form['name']
            gender = request.form['gender']
            birthdate = request.form['birthdate']
            confirm_password = request.form['confirm_password']
            phone = request.form['phone']
            address = request.form['address']
            email = request.form['email']
            diseases = request.form['diseases']
            medications = request.form['medications']
            if password == confirm_password:
                password = password_sha_512_hash(password)
                insert_query = """
                INSERT INTO user (username, password, name, gender, birthdate, confirm_password, phone, address, email, diseases, medications) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                cur.execute(insert_query, (username, password, name, gender, birthdate, confirm_password, phone, address, email, diseases, medications))
                conn.commit()
                msg = "회원가입 성공"
                return render_template('login.html', msg=msg)
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
            username = request.form['username']
            password = request.form['password']
            password = password_sha_512_hash(password)
            select_query = """
            SELECT username FROM user WHERE username = ? AND password = ?
            """
            cur.execute(select_query, (username, password))
            user = cur.fetchone()
            select_query = """
            SELECT COUNT(*) FROM login_logs WHERE u_id = ? AND rdate > DATETIME('now', '-30 minute') 
            """
            cur.execute(select_query, (username, ))
            login_logs_count = cur.fetchone()
            if login_logs_count[0] >= 5 :
                msg = "5회 이상 틀렸습니다. 30분 뒤에 다시 시도 해주세요!"
                return render_template('login.html', msg=msg)
            if user is None:
                insert_query = """
                INSERT INTO login_logs (u_id) 
                VALUES (?)
                """
                cur.execute(insert_query, (username, ))
                conn.commit()
                msg = "로그인 실패"
                return render_template('login.html', msg=msg)
            msg = "로그인 성공"
            session['username'] = user[0]
            return render_template('main.html', msg=msg)
        except sqlite3.IntegrityError:
            msg = "로그인 실패"
            return render_template('login.html', msg=msg)

# 나의 정보 페이지
@app.route('/mypage', methods=['GET', 'POST'])
def mypage():
    if request.method == 'GET':
        username = session['username']
        select_query = """
            SELECT username, password, name, gender, birthdate, confirm_password, phone, address, email, diseases, medications FROM user WHERE username = ?
        """
        cur.execute(select_query, (username, ))
        user_data = cur.fetchone()
        current_user = {
            "username": user_data[0],
            "password": user_data[1],
            "name": user_data[2],
            "gender": user_data[3],
            "birthdate": user_data[4],
            "confirm_password": user_data[5],
            "phone": user_data[6],
            "address": user_data[7],
            "email": user_data[8],
            "diseases": user_data[9],
            "medications": user_data[10]
        }
        print(current_user['birthdate'])
        return render_template('mypage.html', title='나의 페이지', current_user = current_user)
    elif request.method == 'POST':
        username = session['username']
        password = request.form['password']
        name = request.form['name']
        gender = request.form['gender']
        birthdate = request.form['birthdate']
        phone = request.form['phone']
        address = request.form['address']
        email = request.form['email']
        diseases = request.form['diseases']
        medications = request.form['medications']
        password = password_sha_512_hash(password)
        select_query = """
            SELECT password FROM user WHERE username = ?
            """
        cur.execute(select_query, (username, ))
        user_password = cur.fetchone()
        if user_password[0] == password:
            update_query = """
                UPDATE user
                SET name = ?, gender = ?, birthdate = ?, phone = ?, address = ?, email = ?, diseases = ?, medications = ?
                WHERE username = ?;
            """
            cur.execute(update_query, (name, gender, birthdate, phone, address, email, diseases, medications, username))
            conn.commit()
            msg = "수정 성공!!"
        else:
            msg = "수정 실패!!"
        return redirect(url_for('home', msg=msg))

# 로그아웃
@app.route('/logout', methods=['GET'])
def logout():
    if request.method == 'GET':
        session.clear()
        msg = "로그아웃 성공"
        return render_template('main.html', msg=msg)

if __name__ == '__main__':
    app.run('0.0.0.0', port=8000, debug=True)
