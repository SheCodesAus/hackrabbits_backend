from django.db import models
from django.conf import settings

class BaseProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.URLField(max_length=2000, blank=True, null=True)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    industry = models.CharField(max_length=255, blank=True, null=True)
    occupation = models.CharField(max_length=255, blank=True, null=True)
    linkedin_profile = models.URLField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    email_address = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # Ensures this model is only used as a base class


class GeneralProfile(BaseProfile):
    about_me = models.TextField(blank=True, null=True)  # Optional short bio

class RoleModelProfile(BaseProfile):
    journey_summary = models.TextField(blank=True, null=True)  
    skills = models.JSONField(blank=True, null=True)  
    inspiration = models.TextField(blank=True, null=True)  
    certifications = models.JSONField(blank=True, null=True)  
    achievements = models.JSONField(blank=True, null=True)  
    availability = models.JSONField(blank=True, null=True)  