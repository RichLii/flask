from asyncio import FastChildWatcher
from flaskapp.models import User
from flaskapp.extentions import db
from typing import Dict
from flask import request


def add_new_user(user_data: Dict) -> Dict:
    new_user = User(**user_data)
    db.session.add(new_user)
    db.session.commit()
    current_user = get_current_user(
        {'account': user_data.get('account')}).to_dict()
    return current_user


def update_user(id, user_data: Dict):
    current_user = db.session.query(User).filter_by(id=id)
    current_user.update(user_data)
    db.session.commit()
    db.session.close()
    succeed_msg = {'message': '修改成功', 'id': id}
    return succeed_msg


def get_request_data():
    return request.get_json()


def get_current_user(user_data: Dict) -> User:
    return User.query.filter_by(**user_data).first()


def reset_password(user: User, user_data) -> bool:
    if ('password' in user_data.keys()):
        user.password = user_data.password
        return True
    return False
