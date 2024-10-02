from flask import jsonify

from app.Models import Brand
from app.Repository.brand_repository import BrandRepository

class BrandService:
    def __init__(self):
        self.brand_repo = BrandRepository()

    # GET
    def get_all_brands(self):
        brands = self.brand_repo.get_all()
        return [brand.to_dict() for brand in brands]

    # GET by ID
    def get_one_brand(self, brand_id):
        item = BrandRepository.get_by_id(brand_id)
        return item

    # POST
    @staticmethod
    def add_brand(data):
        new_brand = Brand(name=data['name'], image=data['image'], mimetype=data['mimetype'])
        BrandRepository.add_new(new_brand)

    # PUT / PATCH
    @staticmethod
    def update_brand(item_id, data):
        brand = BrandRepository.get_by_id(item_id)
        if not brand:
            return jsonify({'message': 'Desired brand not found'}), 404

        BrandRepository.update_brand(brand, data)

    # DELETE
    @staticmethod
    def delete_fuel(item_id):
        fuel = BrandRepository.get_by_id(item_id)
        if fuel is None:
            return jsonify({'message': 'Brand not found'}), 404

        BrandRepository.remove_brand(fuel)