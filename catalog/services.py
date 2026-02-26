from django.core.cache import cache
from catalog.models import Product
from config.settings import CACHE_ENABLED

def get_products_by_category(category_pk):
    """
    Returns a list of published products for a specific category.
    Uses caching if CACHE_ENABLED is True.
    """
    if not CACHE_ENABLED:
        return Product.objects.filter(category_pk=category_pk, is_published=True)

    key = f'category_{category_pk}_products'
    products = cache.get(key)

    if products is None:
        products = list(Product.objects.filter(category_pk=category_pk, is_published=True))
        cache.set(key, products)

    return products
