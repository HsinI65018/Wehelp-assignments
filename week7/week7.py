from flask import Flask,redirect,render_template,url_for,request,session
from werkzeug.security import check_password_hash, generate_password_hash
import mysql.connector

app = Flask(__name__)
app.secret_key='dev'

connection = mysql.connector.connect(
        host='localhost',
        port='3306',
        user='user',
        password='password',
        database='website'
    )

cursor = connection.cursor(dictionary=True)

### API
@app.route('/api/members', methods=['GET'])
def find_member():
    username = request.args.get('username')
    cursor.execute("SELECT id, username, name FROM member WHERE username=%s", (username,))
    member = cursor.fetchone()
    return {'data': member}

@app.route('/api/member', methods=['POST'])
def update_name():
    new_name = request.get_json(request.data)

    if session.get('username'):
        username = session.get('username')
        cursor.execute("UPDATE member SET name=%s WHERE username=%s", (new_name['name'], username,))
        connection.commit()
        return {"ok": "true"}
    else:
        return {"error": "true"}    

#### old code
@app.route('/')
def home():
    if session.get('username') != None:    
        return redirect(url_for('member'))

    return render_template('home.html') 

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT username FROM member WHERE username=%s",(username,))
        find_username = cursor.fetchone()

        if find_username:
            return redirect(url_for('error', message='帳號已經被註冊'))
        else:     
            cursor.execute("INSERT INTO member (name, username, password) VALUES (%s, %s, %s)"
            ,(name, username, generate_password_hash(password)))
            connection.commit()
            return redirect(url_for('home'))              

    return render_template(url_for('home'))

@app.route('/signin',methods=('GET','POST'))
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT username, password FROM member WHERE username=%s", (username,))
        find_account = cursor.fetchone()

        if username == '' or password == '':
            return redirect(url_for('error',message='請輸入帳號、密碼'))
        elif find_account is None:   
           return redirect(url_for('error',message='帳號、或密碼輸入錯誤' ))    
        elif find_account and check_password_hash(find_account['password'], password):
            session['username'] = username
            return redirect(url_for('member'))
        elif  find_account and check_password_hash(find_account['password'], password) is False:
           return redirect(url_for('error',message='帳號、或密碼輸入錯誤' ))   

    return redirect(url_for('home'))

@app.route('/member')
def member():
    username = session.get('username')
    cursor.execute("SELECT name FROM member WHERE username=%s", (username,))
    name = cursor.fetchone()
    return render_template('member.html', name=name['name'])

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
    app.run(port=3000, debug=True)