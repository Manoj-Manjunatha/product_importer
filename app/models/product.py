"""Product import app Products table."""
from datetime import datetime

from . import db


class Product(db.Model):
    """Table to store products info."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, nullable=False)
    sku = db.Column(db.Unicode, nullable=False, unique=True)
    description = db.Column(db.Unicode)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    modified_at = db.Column(
        db.DateTime, default=datetime.utcnow,
        onupdate=datetime.utcnow, nullable=False
    )
