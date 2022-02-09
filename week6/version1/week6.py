from flask import Flask,redirect,render_template,url_for,request,session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import functools

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:12345678@localhost/website'
app.secret_key='dev'
db = SQLAlchemy(app)

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    account = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, username, account, password):
        self.username = username
        self.account = account
        self.password = password

def signin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get('user_account') is None:
            return redirect(url_for('signin'))

        return view(**kwargs)

    return wrapped_view

@app.route('/')
def home():
    if session.get('user_account') != None:    
        return redirect(url_for('member'))

    return render_template('home.html') 

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        account = request.form['account']
        password = request.form['password']
        if Member.query.filter_by(username=username).first():
            return redirect(url_for('error', message='帳號已經被註冊'))
        else:     
            member = Member(username, account, generate_password_hash(password))
            db.session.add(member)
            db.session.commit()
            return redirect(url_for('home'))

    return render_template(url_for('home'))

@app.route('/signin',methods=('GET','POST'))
def signin():
    if request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        find_account = Member.query.filter_by(account=account).first()

        if account == '' or password == '':
            return redirect(url_for('error',message='請輸入帳號、密碼'))
        elif find_account is None:   
           return redirect(url_for('error',message='帳號、或密碼輸入錯誤' ))    
        elif find_account and check_password_hash(find_account.password, password):
            session['user_account'] = account
            session['username'] = find_account.username
            return redirect(url_for('member'))
        elif  find_account and check_password_hash(find_account.password, password) is False:
           return redirect(url_for('error',message='帳號、或密碼輸入錯誤' ))   

    return redirect(url_for('home'))

@app.route('/member')
@signin_required
def member():
    return render_template('member.html',username=session.get('username'))

@app.route('/error/')
def error():
    error = request.args.get('message')
    error_name = str(error)
    return render_template('error.html',error=error_name)

@app.route('/signout')
def signout():
    session.clear()
    return redirect(url_for('home'))


if __name__ == "__main__":
    db.create_all()
    app.run(port=3000)   