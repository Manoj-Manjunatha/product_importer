"""Product import API."""
import os
from csv import reader
from werkzeug.datastructures import FileStorage

from flask import current_app, jsonify
from flask_restful import abort, reqparse, Resource

from models import db, Product


api_parser = reqparse.RequestParser()
api_parser.add_argument(
    'csv',
    type=FileStorage,
    required=True,
    location='files',
    help='CSV file required'
)


class ProductImportApi(Resource):
    """Import data from csv file, populcate DB."""

    def post(self):
        """."""
        api_data = api_parser.parse_args()
        csv = api_data['csv']
        if csv.mimetype not in ('text/csv', 'application/vnd.ms-excel'):
            abort(412, description='INVALID_FILE')

        try:
            csv_path = os.path.join(current_app.config['MEDIA_FOLDER'], csv.filename)
            csv.save(csv_path)
            with open(csv_path, 'r') as csv_file:
                csv_reader = reader(csv_file)
                headers = csv_reader.next()

                products_dict = {}
                for row in csv_reader:
                    products_dict.update({
                        unicode(row[1]): {
                            'sku': unicode(row[1]),
                            'name': unicode(row[0]),
                            'description': unicode(row[2])
                        }
                    })

                products = Product.query.filter(Product.sku.in_(products_dict.keys())).all()
                for product in products:
                    prod_info = products_dict.pop(product.sku)
                    product.name = prod_info['name']
                    product.description = prod_info['description']
                    db.session.add(product)

                db.session.bulk_insert_mappings(Product, products_dict.values())
                db.session.commit()

        except Exception as e:
            abort(400, description=e.message)

        return jsonify(status='IMPORT_COMPLETE')
