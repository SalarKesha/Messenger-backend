from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, User, AbstractUser
from django.db import models
from django.utils import timezone

from lib.validators import validate_password


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('username is required!')
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username=username, password=password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserModel(AbstractUser):
    OFFLINE = 1
    ONLINE = 2
    BUSY = 3
    STATUS = [
        (OFFLINE, 'offline'),
        (ONLINE, 'online'),
        (BUSY, 'busy')
    ]
    username = models.CharField(unique=True, blank=False, null=False, max_length=36)
    password = models.CharField(max_length=128, validators=[validate_password])
    image = models.ImageField(upload_to='users', blank=True, null=True, default='default/user.jpg')
    status = models.PositiveSmallIntegerField(choices=STATUS, default=OFFLINE)
    last_visit = models.DateTimeField(default=timezone.now)
    objects = UserManager()
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
