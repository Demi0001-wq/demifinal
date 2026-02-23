from rest_framework import serializers
from .models import User, Payment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'telephone', 'city', 'avatar')

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'telephone', 'city', 'avatar')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('session_id', 'payment_link', 'status', 'user', 'payment_date')
