from django.test import TestCase
from users.models import User

class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@example.com")
        self.user.set_password("password")
        self.user.save()

    def test_user_creation(self):
        self.assertEqual(self.user.email, "test@example.com")
        self.assertTrue(self.user.is_active)
