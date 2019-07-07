from .product import ProductApi
from .product_import import ProductImportApi


def configure_api(api_manager):
    """Configure API url endpoints."""
    api_manager.add_resource(
        ProductApi,
        '/api/product',
        '/api/product/',
        '/api/product/<string:sku>'
    )
    api_manager.add_resource(
        ProductImportApi,
        '/api/product-import',
        '/api/product-import/'
    )
