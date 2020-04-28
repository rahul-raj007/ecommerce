from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import os
import random

# Create your models here.


class UserManager(BaseUserManager):

    def create_user(self, email=None, first_name=None, last_name=None, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Email Can't be Empty")
        if not first_name:
            raise ValueError("First Name is Required")
        if not last_name:
            raise ValueError(":Last Name is Required")
        if not password:
            raise ValueError("Password is Required")

        user = self.model(email=self.normalize_email(email),
                          first_name=first_name,
                          last_name=last_name,
                          )

        user.set_password(password)
        user.active = is_active
        user.admin = is_admin
        user.staff = is_staff
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, first_name, last_name, password):
        user = self.create_user(
            email=email, first_name=first_name, last_name=last_name, password=password)
        user.staff = True
        user.admin = False
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        first_name_letter = self.first_name[0].upper()
        last_name = self.last_name.upper()
        return f'{first_name_letter}.{last_name}'

    @property
    def is_active(self):
        return self.active

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


def profile_pic_upload_path(instance, filepath):
    filename = os.path.basename(filepath)
    filename, file_ext = os.path.splitext(filename)
    random_name = random.randint(100, 2546849)
    newfile_name = str(random_name)+file_ext
    return f'profile/{newfile_name}'


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(
        db_index=True,
        max_length=100,
        null=True,
        blank=True
    )
    last_name = models.CharField(
        db_index=True,
        max_length=100,
        null=True,
        blank=True
    )
    DOB = models.DateField(verbose_name="Date Of Birth", blank=True, null=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    unique_id = models.CharField(max_length=20, unique=True)
    profile_pic = models.ImageField(
        upload_to=profile_pic_upload_path, blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
