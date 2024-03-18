from django.contrib.auth.backends import BaseBackend
from .models import AdminUser

# This file contains a custom authentication since we are using custom users
class AdminUserBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = AdminUser.objects.get(username=username)
            if user.check_password(password):
                return user
        except AdminUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return AdminUser.objects.get(pk=user_id)
        except AdminUser.DoesNotExist:
            return None
