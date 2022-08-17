from django.contrib.auth.models import BaseUserManager
from django.db import models
from datetime import datetime


class SoftDeletionQuerySet(models.query.QuerySet):
    def delete(self):
        return super(SoftDeletionQuerySet, self).update(deleted_at=datetime.now(), is_deleted=True)

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)


class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(deleted_at=None, is_deleted=False)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()

    def get_publish(self, email):
        return self.get_queryset().filter(is_deleted=False, email=email).first()


class UserManager(BaseUserManager):
    """
    Custom User Manager for User Model in users/users.py
    """

    def create_user(self, email: str = None, password: str = None, **extra_fields):
        if email is None:
            raise ValueError('email forced.')
        else:
            user = self.model(email=self.normalize_email(email), **extra_fields)

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str = None, password: str = None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('first_name', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True.')

        return self.create_user(email=email, password=password, **extra_fields)
