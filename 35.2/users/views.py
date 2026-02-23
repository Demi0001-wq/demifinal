from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Payment
from .serializers import UserSerializer, UserRegisterSerializer, PaymentSerializer
from .services import create_stripe_product, create_stripe_price, create_stripe_session, retrieve_stripe_session

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
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')
    ordering_fields = ('payment_date',)

class PaymentCreateAPIView(generics.CreateAPIView):
    """
    Endpoint for creating a payment.
    Creates a Stripe product, price, and checkout session.
    Returns the payment link in the response.
    """
    serializer_class = PaymentSerializer

    @extend_schema(
        summary="Create Payment",
        description="Creates a payment and returns a Stripe checkout link.",
        responses={201: PaymentSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        
        # Determine the name of the product
        if payment.paid_course:
            product_name = payment.paid_course.name
        elif payment.paid_lesson:
            product_name = payment.paid_lesson.name
        else:
            product_name = "Generic Payment"

        product_id = create_stripe_product(product_name)
        price_id = create_stripe_price(payment.payment_amount, product_id)
        session_id, payment_link = create_stripe_session(price_id)
        
        payment.session_id = session_id
        payment.payment_link = payment_link
        payment.save()

class PaymentStatusAPIView(generics.RetrieveAPIView):
    """
    Endpoint for checking payment status.
    Retrieves the latest status from Stripe using the session ID.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    @extend_schema(
        summary="Check Payment Status",
        description="Retrieves the current status of a payment from Stripe.",
        responses={200: PaymentSerializer}
    )
    def get(self, request, *args, **kwargs):
        payment = self.get_object()
        if payment.session_id:
            status = retrieve_stripe_session(payment.session_id)
            payment.status = status
            payment.save()
        return super().get(request, *args, **kwargs)
