from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name=models.CharField(max_length=50,null=True)
    picture=models.URLField(max_length=2000,null=True)
    read_only_fields = ('name',)
    class Meta:
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.username