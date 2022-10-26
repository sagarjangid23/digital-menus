from pprint import pprint
from django.db import models
import uuid
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.utils.translation import gettext_lazy as _


# Restaurant Model.
class Restaurant(models.Model):

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    sub_domain = models.CharField(max_length=100, unique=True, error_messages={'unique': 'This sub-domain is already registered.'})

    def __str__(self):
        return self.name


class WebUserManager(BaseUserManager):

    def create_user(self, email, username, password=None, **extra_fields):

        if not email:
            raise ValueError(_('User must have an email address.'))
        
        if not username:
            raise ValueError(_('User must have an Username.'))

        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, username, password, **extra_fields)


class WebUser(AbstractUser):

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, blank=True, null=True)
    is_owner = models.BooleanField(default=False) # restaurant owner.

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = WebUserManager()

    class Meta:
        ordering = ('first_name',)
        verbose_name = 'user'
        verbose_name_plural = 'users'
        unique_together = ("restaurant", "username")

    def __str__(self):
        return self.email