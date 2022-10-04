from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    emails = models.EmailField(unique=True)
