from typing import Optional
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm


def user_login(request: HttpRequest) -> Optional[HttpResponse]:
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
