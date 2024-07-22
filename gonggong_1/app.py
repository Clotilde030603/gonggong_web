from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, current_user

app = Flask(__name__)

@app.context_processor
def inject_user():
    return dict(current_user=current_user)

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/e_intro', methods=['GET', 'POST'])
def e_intro():
    return render_template('e_intro.html', title='기업 소개')

@app.route('/b_intro', methods=['GET', 'POST'])
def b_intro():
    return render_template('b_intro.html', title='사업 소개')

@app.route('/serv1', methods=['GET', 'POST'])
def serv1():
    return render_template('serv1.html', title='서비스1')

@app.route('/serv2', methods=['GET', 'POST'])
def serv2():
    return render_template('serv2.html', title='서비스2')

@app.route('/serv3', methods=['GET', 'POST'])
def serv3():
    return render_template('serv3.html', title='서비스3')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html', titlpe='회원가입')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', title='로그인')

@app.route('/mypage', methods=['GET', 'POST'])
def mypage():
    return render_template('mypage.html', title='나의 페이지')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return render_template('logout.html', title='로그아웃')

if __name__ == '__main__':
    app.run('0.0.0.0', port=8000, debug=True)
