"""Product import main view."""
from flask import Blueprint, render_template, request, url_for
from sqlalchemy import or_

from models import Product

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/<int:page>')
def home(page=None):
    """Render HomePage with upload Ux, and list items."""
    products = Product.query.order_by(Product.id).paginate(page, 20, False)
    next_url = url_for('main.home', page=products.next_num) \
        if products.has_next else None
    prev_url = url_for('main.home', page=products.prev_num) \
        if products.has_prev else None
    template_args = {
        'next_url': next_url,
        'prev_url': prev_url,
        'products': products.items,
        'page_title': 'Products list'
    }
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
