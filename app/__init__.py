import os.path

from flask import Flask, send_from_directory
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    # init
    app = Flask(__name__)

    # Configure database with conn string
    app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=DRIVER%3D%7BODBC%20Driver%2017%20for%20SQL%20Server%7D%3BSERVER%3DLAPTOP-FOXBD%3BDATABASE%3DVerySecureDatabase%3BTrusted_Connection%3Dyes%3BTrustServerCertificate%3Dyes"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # migration for my DB
    # "#flask db history", "#flask db migrate", "#flask db upgrade"
    # all changes inside of temp files in migrations/versions
    db.init_app(app)
    migrate = Migrate(app, db)
    # for encrypting passwords
    bcrypt.init_app(app)

    # generating JWT tokens for logged users
    app.config['JWT_SECRET_KEY'] = 'i_like_turtles' # very secure, much wow
    jwt.init_app(app)

    # Enable CORS for origin localhost:4200, so I can communicate with FE and FE can send requests
    CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})

    # all used models, they are imported inside of Models/__init__.py
    from app.Models import Brand, Item, Car, Fuel, User

    # for me to actually be able to work with multiple routes, they are imported inside of Routes/__init__.py
    from app.Routes import brand_api, fuel_api, car_api, user_api, api
    app.register_blueprint(brand_api)
    app.register_blueprint(fuel_api)
    app.register_blueprint(car_api)
    app.register_blueprint(user_api)
    app.register_blueprint(api)
    
    return app
