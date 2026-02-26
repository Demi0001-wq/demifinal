from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from users.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)


class UserLoginForm(AuthenticationForm):
    pass
