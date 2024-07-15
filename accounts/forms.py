from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=False)
    mobile_number = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('name', 'email', 'mobile_number', 'password1', 'password2', 'birthday', 'pincode')

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        mobile_number = cleaned_data.get('mobile_number')
        if not email and not mobile_number:
            raise forms.ValidationError('Either email or mobile number must be provided.')

class LoginForm(forms.Form):
    email = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())