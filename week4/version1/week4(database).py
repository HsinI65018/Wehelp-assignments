from flask import Flask,redirect,render_template,url_for,request,session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
import functools

app = Flask(__name__)
app.config['SQLALCHEMY_TRAKE_MODIFICATION'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/week4'
app.secret_key = 'dev'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincremant=True)
    account = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False,)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, account, password):
        self.account = account
        self.password = password

def signin_required(func):
    @functools.wraps(func)
    def wrapper(**kwargs):
        if session.get('user_account') is None:
            return redirect(url_for('signin'))
        return func(**kwargs)

    return wrapper        

@app.route('/')
def home():
    user_account = session.get('user_account')
    user_password = session.get('user_account')
    if user_account and user_password:
        return redirect(url_for('member'))

    return render_template('home.html')

# 註冊頁面
@app.route('/register',methods=('GET','POST'))
def register():
    if request.method == 'POST':
        set_account = request.form['account']
        set_password = request.form['password']
        user = User(set_account,generate_password_hash(set_password))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('register.html')    

@app.route('/signin',methods=('GET','POST'))
def signin():
    if request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        fund_user = User.query.filter_by(account=account).first()

        if fund_user and check_password_hash(fund_user.password, password):
            session['user_account'] = account
            session['user_password'] = password
            return redirect(url_for('member'))
        elif account == '' or password == '':
            return redirect(url_for('error',message='請輸入帳號、密碼'))
        elif fund_user and check_password_hash(fund_user.password, password) is False:
            return redirect(url_for('error',message='帳號、或密碼輸入錯誤'))
        elif fund_user == '' and check_password_hash(fund_user.password, password):
            return redirect(url_for('error',message='帳號、或密碼輸入錯誤'))
        else:
            return redirect(url_for('register'))        
                    
    return redirect(url_for('home'))

@app.route('/member')
@signin_required
def member():
    return render_template('member.html')

@app.route('/error/')
def error():
    error = request.args.get('message')
    return render_template('error.html',error=error)        

@app.route('/signout')
def signout():
    session.clear()
    return redirect(url_for('home'))

app.run(port=3000)    