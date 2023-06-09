from django.contrib.auth.models import User
from django.http import HttpRequest


class EmailAuthBackend:
    """auth with email."""

    def authenticate(self, request: HttpRequest, username=None, password=None):
        """чек логина и пароля: хэширует и сравнивает его с бд."""
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

        def get_user(self, user_id):
            try:
                return User.objects.get(pk=user_id)
            except User.DoesNotExist:
                return None
