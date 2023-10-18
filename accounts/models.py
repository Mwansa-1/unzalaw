from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.contrib.auth.models import BaseUserManager , AbstractBaseUser , PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, computer_number, password=None, **extra_fields):
        """
        Creates and saves a User with the given computer_number and password.
        """
        if not computer_number:
            raise ValueError('The Computer Number field must be set')
        if password is None:
            password = "Jumpjet@12"
        user = self.model(computer_number=computer_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, computer_number, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given computer_number and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(computer_number, password, **extra_fields)

    def get_by_natural_key(self, computer_number):
        return self.get(computer_number=computer_number)
    
class CustomUser(AbstractBaseUser , PermissionsMixin):
    computer_number = models.CharField(max_length=100, unique=True)
    # Set password field to null and blank for non-admin users
    password = models.CharField(('password'), max_length=128, null=True, blank=True)
    is_staff = models.BooleanField(default=False)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'computer_number'
    objects = CustomUserManager()

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')

    @property
    def is_anonymous(self):
        return True
    
    @property
    def is_authenticated(self):
        return True
    



class AdminUser(models.Model):
    user_ptr = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        parent_link=True,
    )
    # Add any additional fields for the admin user model here
    pass

    def __str__(self):
        return self.user_ptr.username