"""Product import app CSV table."""
from datetime import datetime

from product_import_app.models import db


class CsvFile(db.Model):
    """Table to store CSV file info."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, nullable=False)
    uuid = db.Column(db.Unicode, nullable=False, unique=True)
    status = db.Column(db.Unicode)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    modified_at = db.Column(
        db.DateTime, default=datetime.utcnow,
        onupdate=datetime.utcnow, nullable=False
    )
