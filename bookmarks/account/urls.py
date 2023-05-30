from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
        path('', include('django.contrib.auth.urls')),
        path('', views.dashboard, name='dashboard'),
        ]

# urlpatterns = [
#     # path('login/', views.user_login, name='login'),
#     path('login/', auth_views.LoginView.as_view(), name='login'),
#     path('logout/', auth_views.LogoutView.as_view(), name='logout'),
#     path('', views.dashboard, name='dashboard'),


#     # url для смены пароля
#     path(
#         'password_change/', auth_views.PasswordChangeView.as_view(),
#         name='password_change'),
#     path(
#         'password_change/done/', auth_views.PasswordChangeDoneView.as_view(),
#         name='password_change_done'),


#     # url сброса пароля
#     path(
#         'password-reset/', auth_views.PasswordResetView.as_view(),
#         name='password_reset'),
#     path(
#         'password-reset/done', auth_views.PasswordResetDoneView.as_view(),
#         name='password_reset_done'),
#     path('password-reset/<uidb64>/<token>/',
#          # проверяет валидность ссылки и передает validlink в контекст
#          auth_views.PasswordResetConfirmView.as_view(),
#          name='password_reset_confirm'),
#     path('password-reset/compelete/',
#          auth_views.PasswordResetCompleteView.as_view(),
#          name='password_reset_complete'),


# ]
