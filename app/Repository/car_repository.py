from app.Models.car import Car, db
from datetime import date

# mimic of all values set on FE
mileage_filters = {
        1: 10000,
        2: 50000,
        3: 100000,
        4: 200000,
        5: 500000
    }

class CarRepository:

    # GET ALL - all optional filters are checked if they were initialized and then are added to sql query,
    # second two sorting options are checked here as well
    def get_all(self, brand=None, lowPrice=None, highPrice=None, mileage=None, model=None, lowYear=None, highYear=None, fuel=None, sortingYear=None, sortingPrice=None):
        query = Car.query
        # Filters if present are added to query that is executed after if statements
        if brand is not None:
            query = query.filter_by(brand=brand) # brand filter is numerical, it checks the ids inside of table Car
        if lowPrice is not None:
            query = query.filter(Car.price > lowPrice)
        if highPrice is not None:
            query = query.filter(Car.price < highPrice)
        if mileage is not None:
            if mileage in mileage_filters:
                query = query.filter(Car.mileage < mileage_filters[mileage]) # mileage set as Array to mimic the one set in FE
        if model is not None:
            query = query.filter(Car.model == model)
        if lowYear is not None:
            query = query.filter(Car.year > lowYear)
        if highYear is not None:
            query = query.filter(Car.year < highYear)
        if fuel is not None:
            query = query.filter(Car.fuel == fuel)

        # sorting here works because both values are numerical and initialized in Car table, so no confusion like Brand
        if sortingYear is not None:
            if sortingYear == 1:
                query = query.order_by(Car.year.asc())
            if sortingYear == 2:
                query = query.order_by(Car.year.desc())
        if sortingPrice is not None:
            if sortingPrice == 1:
                query = query.order_by(Car.price.asc())
            if sortingPrice == 2:
                query = query.order_by(Car.price.desc())

        # query that all filters and sorting made to be displayed in terminal
        print(query)
        return query.all()

    # GET by ID
    def get_by_id(id):
        # using embedded function so all possible errors are already handled
        return Car.query.get_or_404(id)

    # POST
    @staticmethod
    def add_new(car):
        # some variables in class were marked as can be null, just because they are used for GET ALL when getting data
        # from additional tables
        db.session.add(car)
        db.session.commit()
        return car

    # PUT / PATCH
    @staticmethod
    def update_car(car, data):
        # even if data is the same it still gets overwritten, date of change gets written, the only data that remains the
        # same is original user that created the AD, my thinking... admin has option to edit users AD, so user has to remain
        car.brand = data['brand']
        car.model = data['model']
        car.seller = data['seller']
        car.year = data['year']
        car.price = data['price']
        car.fuel = data['fuel']
        car.doorNum = data['doorNum']
        car.description = data['description']
        car.image1 = data['image1']
        car.image2 = data['image2']
        car.image3 = data['image3']
        car.date = date.today()
        car.mileage = data['mileage']
        car.engine = data['engine']
        db.session.commit()

    # DELETE - default implementation nothing was altered
    @staticmethod
    def remove_car(car):
        db.session.delete(car)
        db.session.commit()