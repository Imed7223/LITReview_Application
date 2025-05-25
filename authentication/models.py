from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    SUBSCRIBER = 'SUBSCRIBER'
    ROLE_CHOICES = (
        (SUBSCRIBER, 'Abonné'),
    )
    profile_photo = models.ImageField(verbose_name='Photo de profil', blank=True, null=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='Rôle')