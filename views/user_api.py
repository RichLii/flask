from flaskapp.models import User
from flaskapp.extentions import db
from flask import jsonify, request, Blueprint
from flaskapp.utilities.UserValidator import UserValidator
from flaskapp.utilities.Validator import UniqueValidator
from flaskapp.utilities.module import get_current_user, get_request_data, add_new_user, update_user, reset_password

user_api = Blueprint('user_api', __name__)


# create User
@user_api.route('/user/', methods=['POST'])
def create():
    user_info_dict = get_request_data()
    validator = UserValidator(user_info_dict)
    try:
        validator.nullValidator().uniqueValidator()
    except Exception as e:
        return jsonify(e.args[0]), 400

    new_user = add_new_user(user_info_dict)
    return jsonify({'message': 'created succeed!', **new_user}), 201


# GET User
@user_api.route('/user/', methods=['GET'])
def get_user():
    data = db.session.query(User).all()
    return jsonify([user.to_dict() for user in data]), 200


@user_api.route('/user/<id>', methods=['GET'])
def get_single_user(id):
    current_user = get_current_user({'id': id})
    if current_user:
        return jsonify(current_user.to_dict()), 200
    return jsonify({'message': '查無無此用戶'}), 404


# Update User
@user_api.route('/user/<id>', methods=['PATCH'])
def patch_user(id):
    current_user = get_current_user({'id': id})

    if not current_user:
        return jsonify({'message': '查無無此用戶'}), 404

    user_info_dict = get_request_data()
    validator = UserValidator(user_info_dict)

    try:
        validator.uniqueValidator()
    except Exception as e:
        return jsonify(e.args[0])

    updated_user = update_user(id, user_info_dict)

    return jsonify(updated_user), 200


# Delete User
@user_api.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    user = db.session.query(User).filter_by(id=id).first()

    if not user:
        return jsonify({'message': '查無無此用戶'}), 404

    db.session.delete(user)
    db.session.commit()
    db.session.close()
    return {}, 200


# login api
@user_api.route('/user/login/', methods=["POST"])
def login():
    user_info_dict = get_request_data()

    account = user_info_dict['account']
    password = user_info_dict['password']

    user = User.query.filter_by(account=account).first()

    if not user:
        return jsonify({'message': '無此使用者'}), 404

    if user and user.check_password(password=password):
        return jsonify({'message': '登入成功'}), 200

    return jsonify({'message': '帳號或密碼錯誤'}), 401


#####################

@user_api.route('/password/<id>', methods=["GET"])
def test(id):
    try:
        return User.query.get(id).password
    except Exception as e:
        return jsonify({'message': e.args[0]})


@user_api.route('/test/', methods=['POST'])
def test2():
    account = request.values.get('account')
    password = request.values.get('password')
    return jsonify({'account': account, 'password': password})
