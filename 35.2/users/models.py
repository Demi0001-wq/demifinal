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
    email = models.EmailField(unique=True, verbose_name='Email address')
    
    telephone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Telephone')
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name='City')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Avatar')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('cash', 'Cash'),
        ('transfer', 'Bank Transfer'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments', verbose_name='User')
    payment_date = models.DateField(auto_now_add=True, verbose_name='Payment Date')
    paid_course = models.ForeignKey('materials.Course', on_delete=models.SET_NULL, null=True, blank=True, related_name='payments', verbose_name='Paid Course')
    paid_lesson = models.ForeignKey('materials.Lesson', on_delete=models.SET_NULL, null=True, blank=True, related_name='payments', verbose_name='Paid Lesson')
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Payment Amount')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name='Payment Method')
    
    session_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='Session ID')
    payment_link = models.URLField(max_length=400, blank=True, null=True, verbose_name='Payment Link')
    status = models.CharField(max_length=50, default='pending', verbose_name='Payment Status')

    def __str__(self):
        return f"{self.user} - {self.payment_amount} ({self.payment_date})"

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
