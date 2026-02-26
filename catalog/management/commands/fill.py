import json
from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Fill database with test data'

    @staticmethod
    def json_read_categories():
        with open('catalog/fixtures/catalog_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def json_read_products():
        with open('catalog/fixtures/product_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)

    def handle(self, *args, **options):
        # Clear existing data
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Create categories
        category_for_create = []
        for category in self.json_read_categories():
            category_for_create.append(
                Category(id=category['pk'], **category['fields'])
            )
        Category.objects.bulk_create(category_for_create)

        # Create products
        product_for_create = []
        for product in self.json_read_products():
            product_for_create.append(
                Product(
                    name=product['fields']['name'],
                    description=product['fields']['description'],
                    image=product['fields']['image'],
                    category=Category.objects.get(pk=product['fields']['category']),
                    price=product['fields']['price']
                )
            )
        Product.objects.bulk_create(product_for_create)

        self.stdout.write(self.style.SUCCESS('Successfully filled the database'))
