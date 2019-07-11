"""Product import API."""
import os
from uuid import uuid4
from werkzeug.datastructures import FileStorage

from flask import current_app, jsonify
from flask_restful import abort, reqparse, Resource

from product_import_app.models import CsvFile, db

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
        """Save the csv file, initiate product import."""
        api_data = api_parser.parse_args()
        csv = api_data['csv']
        if csv.mimetype not in ('text/csv', 'application/vnd.ms-excel'):
            abort(412, description='INVALID_FILE')

        try:
            csv_name, ext = os.path.splitext(csv.filename)
            csv_uuid = str(uuid4()) + ext
            csv_path = os.path.join(current_app.config['MEDIA_FOLDER'], csv_uuid)
            csv.save(csv_path)

            csv_file = CsvFile()
            csv_file.name = csv_name
            csv_file.uuid = csv_uuid
            csv_file.status = u'INITIATED'
            db.session.add(csv_file)
            db.session.commit()

            from tasks.product_import import product_import
            product_import.delay({
                'media_folder': current_app.config['MEDIA_FOLDER'],
                'uuid': csv_file.uuid
            })

        except Exception as e:
            abort(400, description=e.message)

        return jsonify(status=csv_file.status)
