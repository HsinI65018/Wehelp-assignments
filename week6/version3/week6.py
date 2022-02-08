from flask import Flask,redirect,render_template,url_for,request,session
from werkzeug.security import check_password_hash, generate_password_hash
import mysql.connector
import functools

app = Flask(__name__)
app.secret_key='dev'

def get_db():
    connection = mysql.connector.connect(
            host='localhost',
            port='3306',
            user='user',
            password='12345678',
            database='website'
        )

    return connection

def close_db():
    connection = get_db()
    connection.close()

    return 'closed'

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
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        username = request.form['username']
        account = request.form['account']
        password = request.form['password']
        cursor.execute("SELECT username FROM member WHERE username=%s",(username,))
        find_username = cursor.fetchone()

        if find_username:
            return redirect(url_for('error', message='帳號已經被註冊'))
        else:     
            cursor.execute("INSERT INTO member (username, account, password) VALUES (%s, %s, %s)"
            ,(username, account, generate_password_hash(password)))
            db.commit()
            close_db()
            return redirect(url_for('home'))              

    return render_template(url_for('home'))

@app.route('/signin',methods=('GET','POST'))
def signin():
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        cursor.execute("SELECT * FROM member WHERE account=%s", (account,))
        find_account = cursor.fetchone()
        close_db()
        
        if account == '' or password == '':
            return redirect(url_for('error',message='請輸入帳號、密碼'))
        elif find_account[2] and check_password_hash(find_account[3], password):
            session['user_account'] = account
            session['username'] = find_account[1]
            return redirect(url_for('member'))
        elif find_account[2] is None and check_password_hash(find_account[3], password):   
            return redirect(url_for('error',message='帳號、或密碼輸入錯誤' ))
        elif  find_account[2] and check_password_hash(find_account[3], password) is False:
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
    app.run(port=3000)