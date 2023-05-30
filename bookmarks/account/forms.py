"""Формы."""
from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    """ Форма для входа в систему. """
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    """форма модели пользователя"""
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        """валидация полей в соответствии с моделью."""
        model = User
        fields = ['username', 'first_name', 'email']


def clean_password2(self):
    """Валидация для совпадения паролей в 2ух полях."""
    cd = self.cleaned_data
    if cd['password'] != cd['password2']:
        raise forms.ValidationError('Passwords dont match.')
    return cd['password2']
