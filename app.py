import os

from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
#database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#initdb
db =SQLAlchemy(app)
#init ma
ma = Marshmallow(app)
#product Class
class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, description,price ,qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty

#product Schema
class ProductSchema(ma.Schema):
    class Meta:
        strict = True
        fields = ('id','name','description', 'price','qty')

#init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

#create end points
#add product
@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    new_product = Product(name, description,price,qty)
    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)
#get product
@app.route('/product', methods= ['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return product_schema.jsonify(product)
#update product
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    product.name = name
    product.description = description
    product.price = price
    product.qty = qty
    db.session.commit()
    return product_schema.jsonify(product)
#delete product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return product_schema.jsonify(product)
# runserver
if __name__ == '__main__':
    app.run(debug=True)