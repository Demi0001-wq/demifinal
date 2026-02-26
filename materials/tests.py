from django.test import TestCase
from materials.models import Course, Lesson
from users.models import User

class MaterialsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@example.com")
        self.course = Course.objects.create(name="Test Course", description="Test Description", owner=self.user)
        self.lesson = Lesson.objects.create(
            name="Test Lesson", 
            description="Test Description", 
            course=self.course, 
            owner=self.user
        )

    def test_course_creation(self):
        self.assertEqual(self.course.name, "Test Course")
        self.assertEqual(self.course.owner, self.user)

    def test_lesson_creation(self):
        self.assertEqual(self.lesson.name, "Test Lesson")
        self.assertEqual(self.lesson.course, self.course)
