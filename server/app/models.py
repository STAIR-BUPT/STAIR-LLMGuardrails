from django.db import models
from django.utils import timezone


def get_default_time():
    return timezone.now()

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=32)
    token = models.CharField(max_length=255, blank=True, null=True)


class Token(models.Model):
    username = models.CharField(max_length=32)
    token = models.CharField(max_length=255, blank=True, null=True)
    createTime = models.DateTimeField(auto_now_add=True)


class Components(models.Model):
    username = models.CharField(max_length=32)
    name = models.CharField(max_length=255, blank=True, null=True)
    initMethod = models.CharField(max_length=500, blank=True, null=True)
    validateMethod = models.CharField(max_length=500, blank=True, null=True)
    createTime = models.DateTimeField(auto_now_add=True)


