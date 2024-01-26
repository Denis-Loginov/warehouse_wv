from flask import render_template, redirect, request
from sqlalchemy.orm import sessionmaker
from models import Products, Inventory, Locations
from app import app, engine

from flask import render_template, redirect, request, url_for
from sqlalchemy.orm import sessionmaker
from models import Products, Inventory, Locations
from app import app, engine

Session = sessionmaker(bind=engine)
session = Session()

# Number of items per page
ITEMS_PER_PAGE = 10

@app.route('/', methods=['GET'])
def index():
    page = request.args.get('page', 1, type=int)
    offset = (page - 1) * ITEMS_PER_PAGE

    groceries = session.query(Products, Inventory, Locations).\
        filter(Inventory.product_id == Products.id).\
        filter(Inventory.location_id == Locations.id).\
        limit(ITEMS_PER_PAGE).offset(offset)

    total_items = session.query(Products).count()
    total_pages = (total_items - 1) // ITEMS_PER_PAGE + 1

    return render_template('index.html', groceries=groceries, page=page, total_pages=total_pages)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        name = request.form['s']
        groceries = session.query(Products, Inventory, Locations).\
            filter(Products.name == name)
        return render_template('search.html', groceries=groceries)
    return render_template('add.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Your existing add route logic
        return redirect('/')
    return render_template('add.html')


@app.route('/delto/<int:inventory_id>', methods=['GET'])
def delete_item(inventory_id):
    inventory_item = session.query(Inventory).filter_by(id=inventory_id).first()

    if inventory_item:
        session.delete(inventory_item)
        session.commit()

    return redirect('/')

@app.route('/addloc', methods=['GET', 'POST'])
def addloc():
    if request.method == 'POST':
        # Your existing addloc route logic
        return redirect('/')
    return render_template('addloc.html')


@app.route('/change', methods=['POST'])
def change():
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        new_quantity = request.form['quantity']

        if product_id and new_quantity:
            product = session.query(Inventory).filter_by(id=product_id).first()

            if product:
                product.quantity = new_quantity
                session.commit()
                return redirect('/')

    return redirect('/')
