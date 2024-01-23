import os

from flask import Flask, request, render_template, redirect

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv

from models import DeclarativeBase, Products, Locations, Inventory

load_dotenv()  # Модуль получения секретных ключей для подключения к БД
user = os.getenv('USER')
password = os.getenv('PASSWORD')

app = Flask(__name__)
connection_string = f'mysql+pymysql://{user}:{password}@localhost/warehousedb'
engine = create_engine(connection_string)
DeclarativeBase.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


@app.route('/', methods=['GET'])
def index():  # Функция вывода всех товаров на странице
    groceries = session.query(Products, Inventory, Locations).\
        filter(Inventory.product_id == Products.id).\
        filter(Inventory.location_id == Locations.id)
    return render_template('index.html', groceries=groceries)


@app.route('/add', methods=['GET', 'POST'])
def add():  # Функция добавления нового продукта
    if request.method == 'POST':
        name = request.form['name']
        desc = request.form['description']
        price = request.form['price']
        quantity = request.form['quantity']
        locations = request.form['locations']
        new_products = Products(name=name, description=desc, price=price)
        new_locations = Locations(name=locations)
        session.add(new_products, new_locations)
        session.commit()
        id_new_products = session.query(Products).\
            order_by(Products.id.desc()).first().id
        id_new_locations = session.query(Locations).\
            order_by(Locations.id.desc()).first().id
        new_quantity = Inventory(
            product_id=id_new_products,
            location_id=id_new_locations,
            quantity=quantity)
        session.add(new_quantity)
        session.commit()
        return redirect('/')
    return render_template('add.html')


@app.route('/addloc', methods=['GET', 'POST'])
def addloc():  # Функция добавления новой локации
    if request.method == 'POST':
        name = request.form['name']
        new_locations = Locations(name=name)
        session.add(new_locations)
        session.commit()
        return redirect('/')
    return render_template('addloc.html')


@app.route('/change', methods=['GET', 'POST'])
def change():  # Функция изменения количества в локации (требует доработки)
    if request.method == 'POST':
        quantity = request.form['quantity']
        old_quantity = session.query().filter_by(Inventory.quantity == '1')
        new_quantity = session.query().\
            update(Inventory(id=old_quantity.id, quantity=quantity))
        session.add(new_quantity)
        session.commit()
        return redirect('/')
    return render_template('change.html')


if __name__ == '__main__':
    app.run(debug=True)
