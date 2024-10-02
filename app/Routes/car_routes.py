from flask import Blueprint, request, jsonify

from app.Models import Car
from app.Routes.brand_routes import brand_service
from app.Services.brand_services import BrandService
from app.Services.car_services import CarService
from app.Services.fuel_services import FuelService
from app.Services.user_services import UserService

car_api = Blueprint('car', __name__)
car_service = CarService()
brand_service = BrandService()
fuel_service = FuelService()
user_service = UserService()

# GET ALL - optional filters and sorting implemented
@car_api.route('/cars', methods=['GET'])
def get_cars():
    # Filters
    brand = request.args.get('brand', type=int)
    lowPrice = request.args.get('lowPrice', type=int)
    highPrice = request.args.get('highPrice', type=int)
    mileage = request.args.get('mileage', type=int)
    model = request.args.get('model', type=str)
    lowYear = request.args.get('lowYear', type=int)
    highYear = request.args.get('highYear', type=int)
    fuel = request.args.get('fuel', type=int)

    # Sorting values can be either null (sort OFF), 1 (sort ASC), 2 (sort DESC), anything else will be ignored (same as OFF)
    sortingBrand = request.args.get('sortingBrand', type=int)
    sortingYear = request.args.get('sortingYear', type=int)
    sortingPrice = request.args.get('sortingPrice', type=int)

    # sending this sausage to service
    cars = car_service.get_all_cars(brand, lowPrice, highPrice, mileage, model, lowYear, highYear, fuel, sortingBrand, sortingYear, sortingPrice)
    return jsonify(cars), 200

# GET by ID - made for retrieving AD information or to Edit existing AD
@car_api.route('/cars/<int:car_id>', methods=['GET'])
def get_one_car(car_id):
    # car array as base
    car = car_service.get_one_car(car_id)

    # calling supporting arrays to get their names and visual images
    brand = brand_service.get_one_brand(car.brand)
    fuel = fuel_service.get_one_fuel(car.fuel)
    seller = user_service.get_one_user(car.seller)

    # with this I made get on FE much less intrusive and easier for resources... I don't need to wait for 4 get requests,
    # but I get everything in one go
    return jsonify({
        'id': car.id,
        'brand': car.brand,
        'brandName': brand.name, # supporting table Brand
        'brandImage': brand.image, # supporting table Brand
        'model': car.model,
        'seller': car.seller,
        'sellerName': seller.name, # supporting table User
        'sellerSurname': seller.surname, # supporting table User
        'sellerTelephone': seller.telephone, # supporting table User
        'year': car.year,
        'price': car.price,
        'fuel': car.fuel,
        'fuelName': fuel.name, # supporting table Fuel
        'doorNum': car.doorNum,
        'description': car.description,
        'image1': car.image1,
        'image2': car.image2,
        'image3': car.image3,
        'date': car.date.isoformat(),
        'mileage': car.mileage,
        'engine': car.engine
    }), 200

# POST - all new data is retrived from FE add form... All checks were already made there so here the job is just to
#       put data to correct places
@car_api.route('/cars', methods=['POST'])
def add_car():
    car = request.get_json()
    CarService.add_car(car)
    return jsonify({'message': 'Car created successfully'}), 201

# PATCH - default method, FE edit form checks for all errors or mistakes, PUT was not implemented
@car_api.route('/cars/<int:car_id>', methods=['PATCH'])
def update_car(car_id):
    data = request.get_json() # data is being sent over in JSON and here it needs array
    CarService.update_car(car_id, data)
    return jsonify({'message': 'Car updated successfully'}), 200

# DELETE - default method, desired id is sent over, only OP or ADMIN have ability to delete a specific AD
@car_api.route('/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    CarService.delete_car(car_id)
    return jsonify({'message': 'Car deleted successfully'}), 201