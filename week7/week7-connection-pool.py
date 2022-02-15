from flask import Flask,redirect,render_template,url_for,request,session
from werkzeug.security import check_password_hash, generate_password_hash
from mysql.connector import pooling, Error

app = Flask(__name__)
app.secret_key='dev'

connection_pool = pooling.MySQLConnectionPool(
    pool_name='week7_pool',
    pool_size=5,
    pool_reset_session=True,
    host='localhost',
    database='website',
    user='user',
    password='password'
)

# 如果有一段 sql 指令 "SELECT id, username, name FROM member WHERE username=%s", (username,)
# sql => "SELECT id, username, name FROM member WHERE username=%s" ，資料型態是 str
# var => (username,) ，資料型態是 list
# type => 要對資料庫做的動作，如果 type=one 代表 fetchone、type=all 代表 fetchall、type=none 代表需要 commit，資料型態是 str

def get_db(sql, var, type):
    try:
        connection_object = connection_pool.get_connection()
        if connection_object.is_connected():
            cursor = connection_object.cursor(dictionary=True)
            cursor.execute(sql, tuple(var))
            if type == 'one':
                return cursor.fetchone()
            elif type == 'all':
                return cursor.fetchall()
            else:
                connection_object.commit()
                return {'200':'commit successfully!'}
    except Error as e:
        print(e)
    finally:
        if connection_object.is_connected():
            cursor.close()
            connection_object.close()
            print('closed connection')  

### API
@app.route('/api/members', methods=['GET'])
def find_member():
    username = request.args.get('username')
    member = get_db("SELECT id, username, name FROM member WHERE username=%s", [username], 'one')
    return {'data': member}

@app.route('/api/member', methods=['POST'])
def update_name():
    new_name = request.get_json(request.data)

    if session.get('username'):
        username = session.get('username')
        check_status = get_db("UPDATE member SET name=%s WHERE username=%s", [new_name['name'],username], 'none')
        print(check_status)
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
        find_username = get_db("SELECT username FROM member WHERE username=%s", [username], 'one')

        if find_username:
            return redirect(url_for('error', message='帳號已經被註冊'))
        else:     
            check_status = get_db("INSERT INTO member (name, username, password) VALUES (%s, %s, %s)", [name,username,generate_password_hash(password)], 'none')
            print(check_status)
            return redirect(url_for('home'))              

    return render_template(url_for('home'))

@app.route('/signin',methods=('GET','POST'))
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        find_ussername = get_db("SELECT username, password FROM member WHERE username=%s", [username], 'one')

        if username == '' or password == '':
            return redirect(url_for('error',message='請輸入帳號、密碼'))
        elif find_ussername is None:   
           return redirect(url_for('error',message='帳號、或密碼輸入錯誤' ))    
        elif find_ussername and check_password_hash(find_ussername['password'], password):
            session['username'] = username
            return redirect(url_for('member'))
        elif  find_ussername and check_password_hash(find_ussername['password'], password) is False:
           return redirect(url_for('error',message='帳號、或密碼輸入錯誤' ))   

    return redirect(url_for('home'))

@app.route('/member')
def member():
    username = session.get('username')
    name = get_db("SELECT name FROM member WHERE username=%s", [username], 'one')
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