import os
from sqlalchemy import Column, String, Integer, create_engine, Boolean,ForeignKey

from flask_sqlalchemy import SQLAlchemy
import json
#####################Psql database configuration #######################################
database_name = 'entertain2'
postgres_username = 'postgres'
postgres_password = '1234'
database_path = 'postgresql://{}:{}@{}/{}'.format( postgres_username, postgres_password,'localhost:5432', database_name)

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

"""
Movies

"""
class Movies(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    thumbnails = Column(String)
    year = Column(Integer)
    category = Column(Integer, ForeignKey('categories.id'))
    rating = Column(String)
    isbookmarked = Column(Boolean, default = False)
    istrending = Column(Boolean, default = False)


    def __init__(self, title, thumbnails, year, category, rating, isbookmarked, istrending):
        self.title = title
        self.thumbnails = thumbnails
        self.year = year
        self.category = category
        self.rating = rating
        self.isbookmarked = isbookmarked
        self.istrending = istrending

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'thumbnails': self.thumbnails,
            'year': self.year,
            'category': self.category,
            'rating': self.rating,
            'isbookmarked':self.isbookmarked,
            'istrending': self.istrending
            }

"""
Category

"""
class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String)


    def __init__(self, type,):
        self.type = type

    def format(self):
        return {
            "id" : self.id, 
            "type" : self.type
            }



class Bookmark(db.Model):
    __tablename__ = 'bookmark'

    id = Column(Integer, primary_key=True)
    name = Column(String)


    def __init__(self, name):
        self.name = name

    def format(self):
        return {
            "id" : self.id, 
            "name" : self.name

            }


class bookmarked(db.Model):
    __tablename__ = 'bookmarked'
    id = Column(Integer, primary_key=True)
    bookmarked_id = Column(Integer, ForeignKey('bookmark.id'))
    movies_id = Column(Integer, ForeignKey('movies.id'))
    create = Column(db.DateTime)

    def __init__(self, name):
        self.name = name,
        self.create = create


    def format(self):
        return {
            "id" : self.id, 
            "name" : self.name,
            }

