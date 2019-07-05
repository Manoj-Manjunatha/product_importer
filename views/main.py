"""Product import main view."""
from flask import Blueprint, render_template

from models import Product

main = Blueprint('main', __name__)


@main.route('/')
def home():
    """Render HomePage with upload Ux, and list items."""
    products = Product.query.filter(Product.is_deleted.__eq__(False)).all()
    template_args = {'products': products}
    return render_template('home.html', **template_args)
