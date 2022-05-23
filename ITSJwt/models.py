from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name=models.CharField(max_length=50,null=True)
    picture=models.URLField(max_length=2000,null=True)
    class Meta:
        swappable = 'AUTH_USER_MODEL'