from flask import Flask
from .extensions import db
from .routes import user
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:12345678@localhost/website2'
    app.secret_key='dev'

    db.init_app(app)

    app.register_blueprint(user)

    return app