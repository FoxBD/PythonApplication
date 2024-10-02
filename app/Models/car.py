from app import db

# main model Car for storing all cars into DB

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.Integer, nullable=False)  # brand is taken from another table Brand
    model = db.Column(db.String(100), nullable=False)
    seller = db.Column(db.Integer, nullable=False) # seller is taken from another table User // for creation user has to be logged in
    year = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=True)
    fuel = db.Column(db.Integer, nullable=False) # fuel is taken from another table Fuel
    doorNum = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    image1 = db.Column(db.Text, nullable=True) # the whole image is saved to BE...
    """
    on FE:  
            - I select an image from file explorer
            - transform it to string
            - read string as data url
    """
    image2 = db.Column(db.Text, nullable=True)
    image3 = db.Column(db.Text, nullable=True)
    date = db.Column(db.Date, nullable=True) # I save only date and no time
    mileage = db.Column(db.Integer, nullable=True)
    engine = db.Column(db.String(100), nullable=True)


    def to_dict(self):
        return {
            'id': self.id,
            'brand': self.brand,
            'brandName': "",
            'model': self.model,
            'seller': self.seller,
            'year': self.year,
            'price': self.price,
            'fuel': self.fuel,
            'doorNum': self.doorNum,
            'description': self.description,
            'image1': self.image1,
            'image2': self.image2,
            'image3': self.image3,
            'date': self.date,
            'mileage': self.mileage,
            'engine': self.engine
        }