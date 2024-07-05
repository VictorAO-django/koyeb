from uuid import uuid4

from django.db import models
from django.core.mail import send_mail,get_connection
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.crypto import get_random_string
from django.core.validators import MinLengthValidator

class UserManager(BaseUserManager):
    def create_user(self, email, password, **other_fields):
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            **other_fields
        )
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self, email, password, **other_fields):
        user = self.create_user(
            email = self.normalize_email(email),
            password=password,
            **other_fields
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.is_verified = True
        user.save(using=self._db)
        return user
    

class User(AbstractUser):
    uuid = models.UUIDField(default=uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(blank=True, max_length=255)
    phone_number = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    is_verified = models.BooleanField(default=False)
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def __str__(self):
        return self.email