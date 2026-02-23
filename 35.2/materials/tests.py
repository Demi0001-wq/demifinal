from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import Group
from users.models import User
from .models import Course, Lesson, Subscription

class MaterialsTestCase(APITestCase):

    def setUp(self):
        # Create Users
        self.user = User.objects.create_user(email='test@example.com', password='testpassword')
        self.moderator_user = User.objects.create_user(email='moderator@example.com', password='testpassword')
        
        # Create Moderator Group
        self.moderator_group, _ = Group.objects.get_or_create(name='Moderator')
        self.moderator_user.groups.add(self.moderator_group)

        # Create Course and Lesson owned by self.user
        self.course = Course.objects.create(name='Test Course', description='Test Description', owner=self.user)
        self.lesson = Lesson.objects.create(name='Test Lesson', description='Test Description', course=self.course, owner=self.user)

    def test_course_create(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('course-list') # Router names usually don't have app prefix if not namespaced
        data = {'name': 'New Course', 'description': 'New Description'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)

    def test_course_list(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('course-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('results' in response.data) # Check pagination results

    def test_lesson_create(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('lesson-create')
        data = {
            'name': 'New Lesson', 
            'description': 'New Description', 
            'course': self.course.id, 
            'video_link': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_create_invalid_video(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('lesson-create')
        data = {
            'name': 'Invalid Lesson', 
            'description': 'Description', 
            'course': self.course.id, 
            'video_link': 'https://vimeo.com/12345'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check that error is present in the response
        self.assertTrue('Video link must be a YouTube link.' in str(response.data))

    def test_subscription_toggle(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('course-subscribe')
        data = {'course': self.course.id}
        
        # Subscribe
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'subscription added')
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())
        
        # Unsubscribe
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'subscription deleted')
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_moderator_permissions(self):
        self.client.force_authenticate(user=self.moderator_user)
        
        # Moderator can view list
        url = reverse('course-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Moderator cannot create course
        data = {'name': 'Mod Course', 'description': 'No'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Moderator cannot delete course
        detail_url = reverse('course-detail', kwargs={'pk': self.course.pk})
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Moderator can edit course
        response = self.client.patch(detail_url, {'name': 'Updated by Mod'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
