import os

from flask import Flask, request, jsonify

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'productdatabase.sqlite')
db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self, name):
        self.name = name


# endpoint to create new product
@app.route("/product", methods=["POST"])
def add_product():
    product = request.json['name']

    new_product = Product(product)

    db.session.add(new_product)
    db.session.commit()

    return {"id": new_product.id, "name": new_product.name}


# endpoint to show all products
@app.route("/product", methods=["GET"])
def get_products():
    all_products = Product.query.all()

    response = []
    for product in all_products:
        product = {"id": product.id, "name": product.name}
        response.append(product)

    return jsonify(response)


# endpoint to get product detail by id
@app.route("/product/<product_id>", methods=["GET"])
def product_detail(product_id):
    product = Product.query.get(product_id)

    return {"id": product.id, "name": product.name}


# endpoint to update product
@app.route("/product/<product_id>", methods=["PUT"])
def product_update(product_id):
    product = Product.query.get(product_id)
    name = request.json['name']

    product.name = name

    db.session.commit()

    return jsonify({"id": product.id, "name": product.name})


# endpoint to delete product
@app.route("/product/<product_id>", methods=["DELETE"])
def product_delete(product_id):
    product = Product.query.get(product_id)
    db.session.delete(product)
    db.session.commit()

    return {"Status": "Success"}


if __name__ == '__main__':
    app.run(debug=True)
