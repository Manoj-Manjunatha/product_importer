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

                for row in csv_reader:
                    sku = unicode(row[1])
                    product = Product.query.filter(Product.sku == sku).first()
                    # If the record exists, then update it.
                    if not product:
                        product = Product()

                    product.sku = sku
                    product.name = unicode(row[0])
                    product.description = unicode(row[2])
                    db.session.add(product)
                db.session.commit()

        except Exception as e:
            abort(400, description=e.message)

        return jsonify(status='IMPORT_COMPLETE')
