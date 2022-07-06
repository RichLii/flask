from requests import get
from new.models import User
from new.extentions import db
from flask import jsonify, request, Blueprint
from new.utilities.module import get_current_user, get_request_data, add_new_user, update_user
from new.utilities.UserValidator import UserValidator

user_api = Blueprint('user_api', __name__)


# create User
@user_api.route('/user/', methods=['POST'])
def create():
    user_info_dict = get_request_data()
    validator = UserValidator(user_info_dict)
    blank_err_msgs = validator.validate_blank()
    duplicate_err_msgs = validator.validate_duplicate()

    if len(blank_err_msgs) != 0:
        return jsonify(blank_err_msgs), 400
    if len(duplicate_err_msgs) != 0:
        return jsonify(duplicate_err_msgs), 400

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
    duplicate_err_msgs = validator.validate_duplicate()

    if len(duplicate_err_msgs) != 0:
        return jsonify(duplicate_err_msgs)

    updated = update_user(id, user_info_dict)

    return jsonify(updated), 200


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
    userData = request.get_json()
    error = validate('account', 'password')
    if error:
        return error

    account = userData['account']
    password = userData['password']

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
