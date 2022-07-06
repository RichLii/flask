from flask import Flask
from .extentions import db, bcrypt, migrate
from .views.user_api import user_api


def create_app():
    app = Flask(__name__)
    app.register_blueprint(user_api)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@192.168.1.193:3308/flaskTwo'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    return app
