from flask import Blueprint,redirect,render_template,url_for,request,session
from werkzeug.security import check_password_hash, generate_password_hash
from .extensions import db
from .model import Member
import functools

user = Blueprint('user', __name__, static_folder='static', template_folder='templates')

def signin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get('user_account') is None:
            return redirect(url_for('user.signin'))

        return view(**kwargs)

    return wrapped_view

@user.route('/')
def home():
    if session.get('user_account') != None:    
        return redirect(url_for('user.member'))

    return render_template('home.html') 

@user.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        account = request.form['account']
        password = request.form['password']
        if Member.query.filter_by(username=username).first():
            return redirect(url_for('user.error', message='帳號已經被註冊'))
        else:     
            member = Member(username, account, generate_password_hash(password))
            db.session.add(member)
            db.session.commit()
            return redirect(url_for('user.home'))

    return render_template(url_for('user.home'))

@user.route('/signin',methods=('GET','POST'))
def signin():
    if request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        find_account = Member.query.filter_by(account=account).first()

        if find_account and check_password_hash(find_account.password, password):
            session['user_account'] = account
            session['username'] = find_account.username
            return redirect(url_for('user.member'))
        elif account == '' or password == '':
            return redirect(url_for('user.error',message='請輸入帳號、密碼'))
        elif find_account == '' and check_password_hash(find_account.password, password):
            return redirect(url_for('user.error',message='帳號、或密碼輸入錯誤' ))
        elif  find_account and check_password_hash(find_account.password, password) is False:
            return redirect(url_for('user.error',message='帳號、或密碼輸入錯誤' ))

    return redirect(url_for('user.home'))

@user.route('/member')
@signin_required
def member():
    return render_template('member.html',username=session.get('username'))

@user.route('/error/')
def error():
    error = request.args.get('message')
    error_name = str(error)
    return render_template('error.html',error=error_name)

@user.route('/signout')
def signout():
    session.clear()
    return redirect(url_for('user.home'))