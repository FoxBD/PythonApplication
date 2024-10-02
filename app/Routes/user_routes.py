from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import datetime
from app.Models.user import User, db
from app.Services.user_services import UserService
from app import bcrypt

user_api = Blueprint('user', __name__)
user_service = UserService()

# GET ALL - method reserved for ADMIN user to check all users
@user_api.route('/users/', methods=['GET'])
def get_users():
    users = user_service.get_all_users()
    return jsonify(users), 200

# GET by ID - method reserved for ADMIN user to edit or delete selected user
@user_api.route('/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    user = user_service.get_one_user(user_id)
    return jsonify({'id': user.id, 'name': user.name, 'surname': user.surname, 'email': user.email, 'password': user.password, 'admin': user.admin, 'telephone': user.telephone}), 200

# DELETE - method reserved for ADMIN user to delete selected user
@user_api.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user_service.delete_user(user_id)
    return jsonify({'message': 'User deleted successfully'}), 201

# PATCH - method reserved for ADMIN user to edit selected user
@user_api.route('/users/<int:users_id>', methods=['PATCH'])
def update_user(users_id):
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"error": "Invalid JSON body"}), 400

    user_service.update_user(users_id, data)
    return jsonify({'message': 'User updated successfully'}), 200

# PATCH - to create user, used by all individuals at the page Register
@user_api.route('/users/register', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
    surname = data.get('surname')
    email = data.get('email')
    password = data.get('password')
    admin = data.get('admin')
    telephone = data.get('telephone')

    # check if new email is already then by anyone else
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 400

    # password encrypted
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(name=name, surname=surname, email=email, password=hashed_password, admin=admin, telephone=telephone)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# POST - for user to LOG IN to application, used by everyone at the page Login, it also creates JWT token for storing in localstorage
@user_api.route('/users/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # user got by filtering it by unique email
    user = User.query.filter_by(email=email).first()

    # then passwords (one in DB and received) are compared if same OK, else ERR
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    # create JWT tokens that expire after one hour, token on FE is stored in localstorage, as well as all other data
    access_token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(hours=1))
    return jsonify({"token": access_token,
                    "id": user.id,
                    "name": user.name,
                    "surname": user.surname,
                    "admin": user.admin,
                    "telephone": user.telephone}), 200
