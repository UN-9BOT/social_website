"""Формы."""
from django import forms


class LoginForm(forms.Form):
    """ Форма для входа в систему. """
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
