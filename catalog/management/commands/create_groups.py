from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='Product Moderator')
        
        content_type = ContentType.objects.get_for_model(Product)
        
        # Permissions to add
        perms = [
            'can_unpublish_product',
            'delete_product',
        ]
        
        for perm_code in perms:
            perm = Permission.objects.get(codename=perm_code, content_type=content_type)
            group.permissions.add(perm)
            
        self.stdout.write(self.style.SUCCESS(f'Group "Product Moderator" created and configured with permissions: {", ".join(perms)}'))
