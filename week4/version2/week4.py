from flask import Flask
from user_package.user import user

app = Flask(__name__)
app.secret_key = 'dev'
app.register_blueprint(user)

@app.route('/test')
def test():
    return 'Hello world!'

if __name__ == '__main__':
    app.run(port=3000)