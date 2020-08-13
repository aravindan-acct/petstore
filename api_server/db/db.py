from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server.models.pet import Pet  # noqa: E501
from swagger_server import util
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin
import __main__  
import os


def db_conn():
    try:
        dbuser = os.environ['DBUSER']
        dbpassword = os.environ['DBPASSWORD']
        dbstring = 'mysql+mysqlconnector://'+dbuser+":"+dbpassword+'@127.0.0.1:3306/awsdevdays'
        engine = db.create_engine(dbstring, echo=True)
    except:
        engine = db.create_engine('mysql+mysqlconnector://pyuser:petstore@127.0.0.1:3306/awsdevdays', echo=True)
    Base = declarative_base()
    return engine, Base

engine, Base = db_conn()

class Pets(Base):
    __tablename__ = 'Pets'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    status = Column(String(50))

    Tags = relationship("Tags", back_populates = 'tag', cascade="all, delete, delete-orphan")
    Photos = relationship("Photos", back_populates = 'photo', cascade="all, delete, delete-orphan")
    #Orders = relationship("Orders", back_populates = 'pet_order', cascade="all, delete, delete-orphan")
    
    def __repr__(self):
        return "<Pets(name='%s', status='%s')>" %(self.name, self.status)

class Tags(Base):
    __tablename__ = 'Tags'

    id = Column(Integer, primary_key=True)
    tag1 = Column(String(50))
    tag2 = Column(String(50))
    pet_id = Column(Integer, ForeignKey('Pets.id'))

    tag = relationship("Pets", back_populates="Tags")
    #Pets.Tags = relationship("Tags", order_by = id, back_populates="tag")
    
    def __repr__(self):
        return "<Tags(tag1='%s', tag2='%s')>" %(self.tag1, self.tag2)


class Photos(Base):
    __tablename__ = 'Photos'

    id = Column(Integer, primary_key=True)
    photo1 = Column(String(100))
    photo2 = Column(String(100))
    pet_id = Column(Integer, ForeignKey('Pets.id'))

    photo = relationship("Pets", back_populates="Photos")
    #Pets.Photos = relationship("Photos", order_by = id, back_populates="photo")
    
    def __repr__(self):
        return "<Photos(photo1='%s', photo2='%s')>" %(self.photo1, self.photo2)

class Users(Base, UserMixin):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    firstName = Column(String(50))
    lastName = Column(String(50))
    email = Column(String(50), unique=True)
    password = Column(String(100))
    phone = Column(Integer)

    #Order_Map = relationship("Order_Map", back_populates = 'user', cascade="all, delete, delete-orphan")

class Orders(Base):
    __tablename__ = 'Orders'

    id = Column(Integer, primary_key=True)
    pet_id = Column(Integer)
    quantity = Column(Integer)
    shipDate = Column(DateTime)
    complete = Column(String(20))
    status = Column(String(20))

    #pet_order = relationship("Pets", back_populates="Orders")
    #Order_Map = relationship("Order_Map", back_populates='order', cascade="all, delete, delete-orphan")

class Order_Map(Base):
    __tablename__ = 'Order_Map'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    order_id = Column(Integer)


Base.metadata.create_all(engine)