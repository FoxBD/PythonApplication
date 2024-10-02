from flask import jsonify

from app.Models import Fuel
from app.Repository.fuel_repository import FuelRepository

class FuelService:
    def __init__(self):
        self.fuel_repo = FuelRepository()

    # GET
    def get_all_fuels(self):
        fuels = self.fuel_repo.get_all()
        return [fuel.to_dict() for fuel in fuels]

    # GET by ID
    def get_one_fuel(self, fuel_id):
        item = FuelRepository.get_by_id(fuel_id)
        return item

    # POST
    @staticmethod
    def add_fuel(data):
        new_fuel = Fuel(name=data['name'])
        FuelRepository.add_new(new_fuel)

    # PUT / PATCH
    @staticmethod
    def update_fuel(item_id, data):
        fuel = FuelRepository.get_by_id(item_id)
        if not fuel:
            return jsonify({'message': 'Desired fuel not found'}), 404

        FuelRepository.update_fuel(fuel, data)

    # DELETE
    @staticmethod
    def delete_fuel(item_id):
        fuel = FuelRepository.get_by_id(item_id)
        if fuel is None:
            return jsonify({'message': 'Fuel not found'}), 404

        FuelRepository.remove_fuel(fuel)