from flask import jsonify
from datetime import date

from app.Repository.car_repository import CarRepository
from app.Models import Car
from app.Services.brand_services import BrandService

brand_service = BrandService()
class CarService:
    def __init__(self):
        self.car_repo = CarRepository()


    # GET ALL - here table Brand is joined to retrieve Name of brand id
    def get_all_cars(self, brand=None, lowPrice=None, highPrice=None, mileage=None, model=None, lowYear=None, highYear=None, fuel=None, sortingBrand=None, sortingYear=None, sortingPrice=None):
        # again sending to repository to retrieve data from DB (MsSql)
        cars = self.car_repo.get_all(brand=brand, lowPrice=lowPrice, highPrice=highPrice, mileage=mileage, model=model, lowYear=lowYear, highYear=highYear, fuel=fuel, sortingYear=sortingYear, sortingPrice=sortingPrice )

        modified_cars = []

        # "join" with table Brand
        for car in cars:
            car_dict = car.to_dict()
            car_dict['brandName'] = brand_service.get_one_brand(car.brand).name
            modified_cars.append(car_dict)

        # had to implement sorting here because else if I'd just look at brand id it would not sort them alphabetically
        if sortingBrand is not None:
            if sortingBrand == 1:
                modified_cars = sorted(modified_cars, key=lambda x: x['brandName'])  # Ascending order
            elif sortingBrand == 2:
                modified_cars = sorted(modified_cars, key=lambda x: x['brandName'], reverse=True)  # Descending order

        return modified_cars

    """
def get_all_cars(self, brand=None, model=None, year=None, sort_by=None, sort_order='asc'):
    # Fetch all cars from the repository
    query = self.car_repo.get_all_query()  # Assume this method returns a query object

    # Apply filters based on provided parameters
    if brand:
        query = query.filter(Car.brand == brand)
    if model:
        query = query.filter(Car.model == model)
    if year:
        query = query.filter(Car.year == year)

    # Apply sorting
    if sort_by:
        if sort_order == 'asc':
            query = query.order_by(getattr(Car, sort_by).asc())
        elif sort_order == 'desc':
            query = query.order_by(getattr(Car, sort_by).desc())

    # Execute the query and convert to dictionary format
    cars = query.all()  # Fetch the filtered and sorted results
    return [car.to_dict() for car in cars]"""

    # GET by ID
    def get_one_car(self, car_id):
        car = CarRepository.get_by_id(car_id)
        return car

    # just a middle man
    @staticmethod
    def add_car(data):
        new_car = Car(
            brand=data['brand'],
            model=data['model'],
            seller=data['seller'],
            year=data['year'],
            price=data['price'],
            fuel=data['fuel'],
            doorNum=data.get('doorNum'),
            description=data.get('description'),
            image1=data.get('image1'),
            image2=data.get('image2'),
            image3=data.get('image3'),
            date=date.today(),
            mileage=data.get('mileage'),
            engine=data.get('engine')
        )
        CarRepository.add_new(new_car)

    # PUT / PATCH
    @staticmethod
    def update_car(car_id, data):
        # desired car to be updated is retrived with GET by ID method in repository
        car = CarRepository.get_by_id(car_id)
        if not car:
            return jsonify({'message': 'Desired car not found'}), 404

        # existing car and new data sent forward to repository
        CarRepository.update_car(car, data)

    # DELETE
    @staticmethod
    def delete_car(car_id):
        # this is new to me, C# .NET is satisfied with id but in here to delete an item it requires the whole item
        car = CarRepository.get_by_id(car_id)
        if car is None:
            return jsonify({'message': 'Car not found'}), 404

        CarRepository.remove_car(car)