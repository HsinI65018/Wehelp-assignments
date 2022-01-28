from flask import Blueprint,redirect,render_template,url_for,request,session
import functools

user = Blueprint('user', __name__, static_folder='static', template_folder='templates')

def signin_required(func):
    @functools.wraps(func)
    def wrapper(**kwargs):
        if session.get('user_account') is None:
            return redirect(url_for('user.signin'))
        return func(**kwargs)

    return wrapper        

@user.route('/')
def home():
    user_account = session.get('user_account')
    user_password = session.get('user_account')
    if user_account and user_password:
        return redirect(url_for('user.member'))

    return render_template('home.html')

@user.route('/signin',methods=('GET','POST'))
def signin():
    if request.method == 'POST':
        account = request.form['account']
        password = request.form['password']

        if account == 'test' and password == 'test':
            session['user_account'] = account
            session['user_password'] = password
            return redirect(url_for('user.member'))
        elif account == '' or password == '':
            return redirect(url_for('user.error',message='請輸入帳號、密碼'))
        elif account != 'test' or password != 'test':
            return redirect(url_for('user.error',message='帳號、或密碼輸入錯誤'))
                    
    return redirect(url_for('user.home'))

@user.route('/member')
@signin_required
def member():
    return render_template('member.html')

@user.route('/error/')
def error():
    error = request.args.get('message')
    return render_template('error.html',error=error)        

@user.route('/signout')
def signout():
    session.clear()
    return redirect(url_for('user.home'))   