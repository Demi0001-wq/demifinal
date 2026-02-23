from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Course, Subscription

@shared_task
def send_course_update_email(course_id):
    """Sends an email notification to all course subscribers when the course is updated."""
    try:
        course = Course.objects.get(pk=course_id)
        subscriptions = Subscription.objects.filter(course=course)
        
        recipient_list = [sub.user.email for sub in subscriptions]
        
        if recipient_list:
            subject = f"Update: Course '{course.name}' has been updated"
            message = f"Hello! We wanted to let you know that the materials for the course '{course.name}' have been updated. Check them out now!"
            from_email = settings.EMAIL_HOST_USER
            
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipient_list,
                fail_silently=False,
            )
            print(f"Emails sent to {len(recipient_list)} subscribers of course '{course.name}'.")
        else:
            print(f"No subscribers found for course '{course.name}'.")
            
    except Course.DoesNotExist:
        print(f"Course with ID {course_id} does not exist.")
