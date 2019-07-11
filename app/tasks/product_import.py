"""Product import Celery task."""
import os
from csv import reader

from app import celery
from models import CsvFile, db, Product


@celery.task(queue='import')
def product_import(csv_data):
    """Read csv file, create/update DB records."""
    csv_record = CsvFile.query.filter(CsvFile.uuid == csv_data['uuid']).first()
    try:
        csv_path = os.path.join(csv_data['media_folder'], csv_data['uuid'])
        with open(csv_path, 'r') as csv_file:
            csv_reader = reader(csv_file)
            _headers = csv_reader.next()

            if not csv_record:
                raise Exception(message='NO_RECORD')

            csv_record.status = u'PROGRESS'
            db.session.add(csv_record)
            db.session.commit()

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
            csv_record.status = u'COMPLETED'
            db.session.add(csv_record)

    except Exception as e:
        print e.message
        csv_record.status = u'FAILED'
        db.session.add(csv_record)

    finally:
        db.session.commit()
