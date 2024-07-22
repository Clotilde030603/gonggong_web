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
    return render_template('e_intro.html', title='Enterprise Intro')

@app.route('/b_intro', methods=['GET', 'POST'])
def b_intro():
    return render_template('b_intro.html', title='Business Intro')

@app.route('/serv1', methods=['GET', 'POST'])
def serv1():
    return render_template('serv1.html', title='Service1')

@app.route('/serv2', methods=['GET', 'POST'])
def serv2():
    return render_template('serv2.html', title='Service2')

@app.route('/serv3', methods=['GET', 'POST'])
def serv3():
    return render_template('serv3.html', title='Service3')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html', titlpe='Register')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', title='Login')

@app.route('/mypage', methods=['GET', 'POST'])
def mypage():
    return render_template('mypage.html', title='Edit Profile')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return render_template('logout.html', title='Logout')

if __name__ == '__main__':
    app.run('0.0.0.0', port=8000, debug=True)
