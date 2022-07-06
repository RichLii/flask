from .extentions import db
from sqlalchemy.orm import validates
from new import bcrypt


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    account = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    active = db.Column(db.Boolean, default=True)

    def to_dict(self, *columns):
        if len(columns) == 0:
            columns = ['id', 'account', 'username']
        return {col: getattr(self, col) for col in list(filter(lambda x: x in columns, self.__table__.columns.keys()))}

    @ property
    def password(self):
        raise AttributeError('password is not readable attribute')

    @ password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(
            password).decode('utf8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %s>' % self.username
