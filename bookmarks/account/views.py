from typing import Optional
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import (LoginForm, UserRegistrationForm,
                    UserEditForm, ProfileEditForm)
from .models import Profile


@login_required
def edit(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,  # type: ignore
            data=request.POST,
            files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
            instance=request.user.profile)  # type: ignore
    return render(
        request, 'account/edit.html',
        {'user_form': user_form, 'profile_form': profile_form})


def register(request: HttpRequest) -> HttpResponse:
    """ стандартная регистрация с хешированием пароля. """
    if request.method == 'POST':
        user_form: UserRegistrationForm = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создание обьекта юзера без сохранения.
            new_user: User = user_form.save(commit=False)
            # установка выбранного пароля и хэширование PBKDF2.
            new_user.set_password(user_form.cleaned_data['password'])
            # save obj User
            new_user.save()
            # Создние профиля пользователя, который будет ассоциирован с User
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html',
                  {'user_form': user_form})


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    """
    Если в запросе нет параметра next перенаправляет их на дашбоард.

    Для этого в templates определен атрибут next.
    """
    if request.user.is_authenticated:
        print("***\nye\n***")
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


def user_login(request: HttpRequest) -> HttpResponse:
    """
    Вход в систему.

    GET: создание экземпляра новой формы входа и передача в шаблон.

    POST:
        1. Забор данных из запроса и создание экземпляра формы.
        2. Валидация.
        3. Аутентификация. Если пользователь существует то возвращает обьект
            класса User. Или ответ что неверный логин.
        4. Если пользователь не активен(заблочен), то Disabled account.
        5. Создание сеанса если всё успешно.
    """
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user: Optional[AbstractBaseUser] = authenticate(
                request, username=cd['username'], password=cd['password'])
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Autheticated successully')
                else:
                    return HttpResponse('Disabled account')

            else:
                return HttpResponse('Invalid login or password')

    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})
