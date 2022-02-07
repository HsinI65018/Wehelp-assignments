from datetime import datetime
from .extensions import db

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