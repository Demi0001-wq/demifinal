from django.db import models
from django.conf import settings

class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name')
    preview = models.ImageField(upload_to='courses/', blank=True, null=True, verbose_name='Preview')
    description = models.TextField(verbose_name='Description')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Owner')

    def __str__(self):
        return self.name

class Lesson(models.Model):
    name = models.CharField(max_length=255, verbose_name='Name')
    description = models.TextField(verbose_name='Description')
    preview = models.ImageField(upload_to='lessons/', blank=True, null=True, verbose_name='Preview')
    video_link = models.URLField(verbose_name='Video link', blank=True, null=True)
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name='Course')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Owner')

    def __str__(self):
        return self.name

class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='User')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Course')

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
        unique_together = ('user', 'course')

    def __str__(self):
        return f'{self.user} - {self.course.name}'
