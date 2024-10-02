from app.Models.user import User, db

class UserRepository:
    def get_all(self):
        return User.query.all()

    # GET by ID
    def get_by_id(id):
        return User.query.get_or_404(id)

    # PUT / PATCH
    @staticmethod
    def update_user(user, data):
        user.name = data['name']
        user.surname = data['surname']
        user.email = data['email']
        user.password = data['password']
        user.admin = data['admin']
        user.telephone = data['telephone']
        db.session.commit()

    # DELETE
    @staticmethod
    def remove_user(user):
        db.session.delete(user)
        db.session.commit()