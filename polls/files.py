from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


# Create your forms here.

# It creates a new user form with the fields username, email, password1, and password2.
class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    from django import forms
    from django.contrib.auth.forms import UserCreationForm

    class MyUserCreationForm(UserCreationForm):
        email = forms.EmailField()

        class Meta:
            model = User
            fields = ['username', 'email', 'password1', 'password2']


# It creates a class called LoginForm that inherits from the AuthenticationForm class.
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
