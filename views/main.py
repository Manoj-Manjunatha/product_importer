"""Product import main view."""
from flask import Blueprint, render_template, request
from sqlalchemy import or_

from models import Product

main = Blueprint('main', __name__)


@main.route('/')
def home():
    """Render HomePage with upload Ux, and list items."""
    products = Product.query.order_by(Product.id).all()
    template_args = {'products': products, 'page_title': 'Products list'}
    return render_template('home.html', **template_args)


@main.route('/search')
def search():
    """Search the DB records matching the keyword."""
    keyword = request.args.get('keyword')
    products = Product.query.filter(
        or_(
            Product.name.ilike('%{}%'.format(keyword)),
            Product.sku.ilike('%{}%'.format(keyword)),
            Product.description.ilike('%{}%'.format(keyword))
        )
    ).all()
    return render_template('home.html', **{
        'products': products,
        'page_title': 'Search results'
    })
