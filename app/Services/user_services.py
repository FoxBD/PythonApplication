from flask import jsonify

from app import bcrypt
from app.Models import User
from app.Repository.user_repository import UserRepository

class UserService:
    def __init__(self):
        self.user_repo = UserRepository()

    def get_all_users(self):
        users = self.user_repo.get_all()
        return [user.to_dict() for user in users]

    def get_one_user(self, user_id):
        user = UserRepository.get_by_id(user_id)
        return user

    @staticmethod
    def update_user(item_id, data):
        user = UserRepository.get_by_id(item_id)

        # two checks first if it actually exists in DB
        if not user:
            return jsonify({'message': 'Desired user not found'}), 404

        # second to check if new email is already then by anyone else
        existing_user = User.query.filter(User.email == data["email"], User.id != item_id).first()
        if existing_user:
            return jsonify({"error": "User with this email already exists"}), 400

        # new password encrypted by same step as create user
        hashed_password = bcrypt.generate_password_hash(data["password"]).decode('utf-8')
        data["password"] = hashed_password

        try:
            UserRepository.update_user(user, data)
        except Exception as e:
            return jsonify({'error': e}), 500

        return jsonify({'message': 'User updated successfully'}), 200

    # DELETE
    @staticmethod
    def delete_user(item_id):
        user = UserRepository.get_by_id(item_id)
        if user is None:
            return jsonify({'message': 'User not found'}), 404

        UserRepository.remove_user(user)