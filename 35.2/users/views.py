from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import User, Payment
from .serializers import *
from .services import *
class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)
class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        product_name = payment.paid_course.name if payment.paid_course else payment.paid_lesson.name if payment.paid_lesson else "Generic Payment"
        product_id = create_stripe_product(product_name)
        price_id = create_stripe_price(payment.payment_amount, product_id)
        session_id, payment_link = create_stripe_session(price_id)
        payment.session_id, payment.payment_link = session_id, payment_link
        payment.save()
class PaymentStatusAPIView(generics.RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    def get(self, request, *args, **kwargs):
        payment = self.get_object()
        if payment.session_id:
            payment.status = retrieve_stripe_session(payment.session_id)
            payment.save()
        return super().get(request, *args, **kwargs)
