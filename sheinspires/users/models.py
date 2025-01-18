from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser): 
    USER_TYPE_CHOICES = {
        "ADMIN": "Admin",
        "ROLE_MODEL": "Role Model",
        "COMMUNITY_USER": "Community User",
    }
    user_type = models.CharField(
        max_length=1,
        choices=USER_TYPE_CHOICES,
        default="COMMUNITY_USER",
    )

    image = models.URLField(max_length=2000, blank=True, null=True)
    current_role = models.CharField(max_length=50)
    inspiration = models.CharField(max_length=200)
    advice = models.CharField(max_length=200)
   
    LOCATION_CHOICES = {
        "WA": "Western Australia",
        "SA": "South Australia",
        "VIC": "Victoria",
        "TAS": "Tasmania",
        "ACT": "Australian Capital Territory",
        "NSW": "New South Wales",
        "QLD": "Queensland",
        "NT": "Northern Territory",
    }
    location = models.CharField(
        max_length=1,
        choices=LOCATION_CHOICES,
    )

    phone_number = models.CharField(max_length=10)
    linkedin = models.CharField(max_length=200)
