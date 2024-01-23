import sqlalchemy
from sqlalchemy import Column, Integer, String, Text, DECIMAL, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = sqlalchemy.orm.declarative_base()


class Products (DeclarativeBase):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column('name', String(50))
    description = Column('description', Text)
    price = Column('price', DECIMAL)


class Locations (DeclarativeBase):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    name = Column('name', String(50))


class Inventory (DeclarativeBase):
    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True)
    product_id = Column('product_id', Integer, ForeignKey('products.id'))
    location_id = Column('location_id', Integer, ForeignKey('locations.id'))
    quantity = Column('quantity', Integer)
