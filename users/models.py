from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    payment_date = models.DateField(auto_now_add=True)
    paid_course = models.ForeignKey('materials.Course', on_delete=models.SET_NULL, null=True, blank=True)
    paid_lesson = models.ForeignKey('materials.Lesson', on_delete=models.SET_NULL, null=True, blank=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(
        max_length=20,
        choices=(('cash', 'Cash'), ('transfer', 'Bank Transfer'))
    )
    session_id = models.CharField(max_length=255, blank=True, null=True)
    payment_link = models.URLField(max_length=400, blank=True, null=True)
    status = models.CharField(max_length=50, default='pending')
