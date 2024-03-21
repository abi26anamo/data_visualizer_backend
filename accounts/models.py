from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _


class UserAccountManager(BaseUserManager):
    """
    Custom manager for UserAccount model.
    Provides methods to create regular users and superusers.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a regular user with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class UserAccount(AbstractUser, PermissionsMixin):
    """
    Custom user model inheriting from AbstractUser and PermissionsMixin.
    """
    username = None
    email = models.EmailField(max_length=255, unique=True)

    objects = UserAccountManager()

    USERNAME_FIELD = "email"  # The field to use as the unique identifier for user authentication
    REQUIRED_FIELDS = []  # Specifies the fields required when creating a user via the command line

    def __str__(self):
        """
        Returns the string representation of the user (email).
        """
        return self.email

    def save(self, *args, **kwargs):
        """
        Overrides the save method to ensure lowercase email addresses.
        """
        self.email = self.email.lower()  # Convert email to lowercase
        return super(UserAccount, self).save(*args, **kwargs)  # Calls the parent class's save method
