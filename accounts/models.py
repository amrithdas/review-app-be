from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email=None, mobile_number=None, name=None, password=None, birthday=None, pincode=None):
        """
        Creates and saves a user with the given email, mobile number, name, and password.
        """
        if not email and not mobile_number:
            raise ValueError('Either email or mobile number must be set')
        if not name:
            raise ValueError('Name must be set')

        user = self.model(
            email=self.normalize_email(email) if email else None,
            mobile_number=mobile_number,
            name=name,
            birthday=birthday,
            pincode=pincode,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, name, and password.
        """
        user = self.create_user(
            email=email,
            name=name,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    mobile_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)  # New field for birthday
    pincode = models.CharField(max_length=10, blank=True, null=True) 

    USERNAME_FIELD = 'email'  # Use email as the default username field
    REQUIRED_FIELDS = ['name']  # Require name when creating users

    objects = CustomUserManager()
    pass

    def __str__(self):
        return self.name
