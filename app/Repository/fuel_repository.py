from app.Models.fuel import Fuel, db

class FuelRepository:
    # GET
    def get_all(self):
        return Fuel.query.all()

    # GET by ID
    def get_by_id(id):
        return Fuel.query.get_or_404(id)

    # POST
    @staticmethod
    def add_new(fuel):
        db.session.add(fuel)
        db.session.commit()
        return fuel

    # PUT / PATCH
    @staticmethod
    def update_fuel(fuel, data):
        fuel.name = data['name']
        db.session.commit()

    # DELETE
    @staticmethod
    def remove_fuel(fuel):
        db.session.delete(fuel)
        db.session.commit()