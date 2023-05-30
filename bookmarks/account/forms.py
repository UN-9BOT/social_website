"""Формы."""
from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserEditForm(forms.ModelForm):
    """форма для редактирования информации для встроенной модели User."""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        """Запрет на создание профиля с таким же email."""
        data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id).filter(email=data)
        if qs.exists():
            raise forms.ValidationError('Email already in use')
        return data


class ProfileEditForm(forms.ModelForm):
    """Редактирование данных в форме Profile."""
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']


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

    def clean_email(self):
        """Запрет на создание профиля с таким же email."""
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("Email already in use.")
        return data
