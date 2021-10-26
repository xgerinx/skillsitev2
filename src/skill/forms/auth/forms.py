from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class AuthForm(forms.ModelForm):

    class Meta:
        password = forms.CharField(widget=forms.PasswordInput)
        model = User
        widgets = {
            'password': forms.PasswordInput(),
        }
        fields = ('email', 'password')


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean(self):
        """Check if email is unique"""
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return cleaned_data
