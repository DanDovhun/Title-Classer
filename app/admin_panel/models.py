from django.db import models
from django.contrib.auth.models import AbstractUser

class AdminUser(AbstractUser):

    #fix for reverse relations clash
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='admin_users',
        related_query_name='admin_user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='admin_users',
        related_query_name='admin_user'
    )

    def __str__(self):
        return self.username