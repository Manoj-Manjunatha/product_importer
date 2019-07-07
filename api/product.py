"""Product import API."""
from flask import jsonify
from flask_restful import abort, fields, marshal, Resource, reqparse


from models import db, Product


product_fields = {
    'name': fields.String,
    'sku': fields.String,
    'description': fields.String
}


api_parser = reqparse.RequestParser()
api_parser.add_argument(
    'name',
    required=True,
    location='form',
    type=unicode,
    help='Please provide the name of the Product.'
)
api_parser.add_argument(
    'sku',
    required=True,
    location='form',
    type=unicode,
    help='Please provide the sku of the Product.'
)
api_parser.add_argument(
    'description',
    location='form',
    type=unicode,
)


class ProductApi(Resource):
    """API to handle GET, POST, PUT, DELETE."""

    def get(self, sku=None):
        """
        Return products info.

        Return a product info if 'sku' is not None,
        else return all products info.
        """
        products = []
        if sku:
            product = Product.query.filter(Product.sku == sku).first_or_404()
            products.append(product)
        else:
            products = Product.query.order_by(Product.id).all()

        return marshal(products, product_fields), 200

    def post(self):
        """Create a product record."""
        post_data = api_parser.parse_args()

        # Check if the product sku exits,
        # if it exits then throw an error,
        # else create one.
        product = Product.query.filter(Product.sku == post_data['sku']).first()
        if product:
            abort(400, description='Product Exists')

        product = Product()
        product.name = post_data['name']
        product.sku = post_data['sku']
        product.description = post_data.get('description')
        db.session.add(product)
        db.session.commit()

        return marshal(product, product_fields), 201

    def put(self, sku):
        """Modify name, desciption of a product."""
        put_data = api_parser.parse_args()
        product = Product.query.filter(Product.sku == put_data['sku']).first_or_404()
        product.name = put_data['name']
        product.description = put_data.get('description')
        db.session.add(product)
        db.session.commit()

        return marshal(product, product_fields), 200

    def delete(self, sku):
        """Remove the product from DB. Hard Delete."""
        _data = api_parser.parse_args()

        product = Product.query.filter(Product.sku == _data['sku']).first_or_404()
        db.session.delete(product)
        db.session.commit()

        return jsonify(status='DELETED')
