from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

# Base User Model
class CustomUser(AbstractUser):
    USER_TYPES = {
        "ADMIN": "Admin",
        "ROLE_MODEL": "Role Model",
        "COMMUNITY_USER": "Community User",
    }
    user_type = models.CharField(max_length=20, choices=USER_TYPES) # Do we need a default user here?
    # first_name = models.CharField(max_length=50) --- included in AbstractUser model
    # last_name = models.CharField(max_length=50)
    image = models.URLField(blank=True, null=True)  # URL to profile image
    # tagline = models.CharField(max_length=100) --- do we want to include?
    current_role = models.CharField(max_length=100)
    inspiration = models.TextField(blank=True, null=True)
    advice = models.TextField(blank=True, null=True)

    LOCATIONS = {
        "PERTH": "Perth",
        "ADELAIDE": "Adelaide",
        "MELBOURNE": "Melbourne",
        "HOBART": "Hobart",
        "CANBERRA": "Canberra",
        "SYDNEY": "Sydney",
        "BRISBANE": "Brisbane",
        "DARWIN": "Darwin",
    }
    location = models.CharField(max_length=100, choices=LOCATIONS)

    phone_number = models.CharField(max_length=20, blank=True, null=True)
    # email = models.EmailField(unique=True) --- included in AbstractUser model
    linkedin = models.URLField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user_type})"

# ALL USER DATA

# Categories
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UserCategory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_categories")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_users")

# Industries
class Industry(models.Model):
    name = models.CharField(max_length=100)
    badge_icon = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class UserIndustry(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_industries")
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, related_name="industry_users")

# ROLE MODEL SPECIFIC DATA

# Milestones
class Milestone(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    milestone_date = models.DateField()

    def __str__(self):
        return self.name

class UserMilestone(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_milestones")
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE, related_name="milestone_users")

# Achievements
class Achievement(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UserAchievement(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_achievements")
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name="achievement_users")

# Skills
class Skill(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class UserSkill(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_skills")
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name="skill_users")


