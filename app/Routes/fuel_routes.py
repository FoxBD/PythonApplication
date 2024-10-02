from flask import Blueprint, request, jsonify
from app.Services.fuel_services import FuelService

fuel_api = Blueprint('fuel', __name__)
fuel_service = FuelService()

# brand, fuel are both the same - look for brand_routes.py
@fuel_api.route('/fuels', methods=['GET'])
def get_fuels():
    fuels = fuel_service.get_all_fuels()
    return jsonify(fuels), 200

@fuel_api.route('/fuels/<int:fuel_id>', methods=['GET'])
def get_one_fuel(fuel_id):
    fuel = fuel_service.get_one_fuel(fuel_id)
    return jsonify({'id': fuel.id, 'name': fuel.name}), 200


@fuel_api.route('/fuels', methods=['POST'])
def add_fuel():
    fuel = request.get_json()
    FuelService.add_fuel(fuel)
    return jsonify({'message': 'Fuel created successfully'}), 201


@fuel_api.route('/fuels/<int:fuel_id>', methods=['PATCH'])
def update_item(fuel_id):
    data = request.get_json()
    FuelService.update_fuel(fuel_id, data)
    return jsonify({'message': 'Fuel updated successfully'}), 200


@fuel_api.route('/fuels/<int:fuel_id>', methods=['DELETE'])
def delete_item(fuel_id):
    FuelService.delete_fuel(fuel_id)
    return jsonify({'message': 'Fuel deleted successfully'}), 201