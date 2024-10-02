
import os
basedir = os.path.abspath(os.path.dirname(__file__))

# class Config not doing much, was generated, but real conn string is inside __init__.py
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'app.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
