from flask import Blueprint, request, jsonify
from app.Services.brand_services import BrandService

brand_api = Blueprint('brand', __name__)
brand_service = BrandService()

# brand, fuel are both the same - for both I'll explain it here

# GET ALL
@brand_api.route('/brands', methods=['GET'])
def get_brands():
    brands = brand_service.get_all_brands()
    return jsonify(brands), 200

# GET by ID
@brand_api.route('/brands/<int:brand_id>', methods=['GET'])
def get_one_brand(brand_id):
    brand = brand_service.get_one_brand(brand_id)
    return jsonify({'id': brand.id, 'name': brand.name, 'image': brand.image, 'mimetype': brand.mimetype}), 200

# POST
@brand_api.route('/brands', methods=['POST'])
def add_brand():
    brand = request.get_json()
    BrandService.add_brand(brand)
    return jsonify({'message': 'Brand created successfully'}), 201

# PATCH
@brand_api.route('/brands/<int:brand_id>', methods=['PATCH'])
def update_item(brand_id):
    data = request.get_json()
    BrandService.update_brand(brand_id, data)
    return jsonify({'message': 'Brand updated successfully'}), 200

# DELETE
@brand_api.route('/brands/<int:brand_id>', methods=['DELETE'])
def delete_item(brand_id):
    BrandService.delete_fuel(brand_id)
    return jsonify({'message': 'Brand deleted successfully'}), 201
