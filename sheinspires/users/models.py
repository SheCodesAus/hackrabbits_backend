from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


# Create your models here.
class CustomUser(AbstractUser):
    USER_TYPES = (
        ("ADMIN", "Admin"),
        ("ROLE_MODEL", "Role Model"),
        ("COMMUNITY_USER", "Community User"),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default="COMMUNITY_USER") 
    
    # Q DS: Do we need a default user here? 
    # Answer BS: default user added to avoid validation error


    # first_name = models.CharField(max_length=50) --- included in AbstractUser model
    # last_name = models.CharField(max_length=50)
    
    image = models.URLField(blank=True, null=True)  # URL to profile image
    
    # tagline = models.CharField(max_length=100) --- do we want to include?
    
    current_role = models.CharField(max_length=100)
    inspiration = models.TextField(blank=True, null=True)
    advice = models.TextField(blank=True, null=True)

    # Many to Many Fields for Categories
    # Allows users to choose multiple Categories (using a checkbox for example)
    categories = models.ManyToManyField('Category', blank=True)

    # Using CHOICES option here so that users only have one choice each for Industries and Locations
    INDUSTRIES = (
        ("EDUCATION", "Education"),
        ("HEALTHCARE", "Healthcare"),
        ("CYBER_SECURITY", "Cyber Security"),
        ("SOFTWARE_ENGINEERING", "Software Engineering"),
        ("DATA_SCIENCE", "Data Science"),
        ("FINANCE", "Finance"),
        ("AI", "AI"),
        ("ENERGY", "Energy"),
        ("TRANSPORTATION", "Transportation"),
        ("VIDEO_GAME_DEV", "Video Game Development"),
        ("GOVERNMENT", "Government"),
        ("MEDIA_ENTERTAINMENT", "Media & Entertainment"),
        ("STARTUP", "Startup"),
        ("NON_PROFIT", "Non-Profit"),
    )
    industry = models.CharField(max_length=100, choices=INDUSTRIES,blank=True,
    null=True,
    # default="SOFTWARE_ENGINEERING"
    )

    LOCATIONS = (
        ("PERTH", "Perth"),
        ("ADELAIDE", "Adelaide"),
        ("MELBOURNE", "Melbourne"),
        ("HOBART", "Hobart"),
        ("CANBERRA", "Canberra"),
        ("SYDNEY", "Sydney"),
        ("BRISBANE", "Brisbane"),
        ("DARWIN", "Darwin"),
    )
    location = models.CharField(max_length=100, choices=LOCATIONS, blank=True,
    null=True,
    # default="PERTH"
    )


# Q BS: how about adding a line choose location as default value?


    phone_number = models.CharField(
        max_length=20,
          blank=True, null=True,
          validators=[
              RegexValidator(
                  regex=r"^\+?1?\d{9,15}$",
                  message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
                  )
                    ],
                    )
    
    # email = models.EmailField(unique=True) --- included in AbstractUser model
    linkedin = models.URLField(blank=True, null=True)

    date_joined = models.DateTimeField(auto_now_add=True)

    # ROLE MODEL FIELDS ONLY (but still within CustomUser class)
    # Note the Many to Many Field for Skills
    # Like Categories above, this allows users to choose multiple Skills (using a checkbox for example)

    milestones = models.TextField(blank=True, null=True)
    achievements = models.TextField(blank=True, null=True)
    skills = models.ManyToManyField('Skill', blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user_type})"



# Skills and Categories models so that both fields inside the CustomUser model can have multiple values stored when a user signs up
# aka - A user can select multiple skills and/or categories during the sign-up process 

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Skill Model
class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# # Call this function manually after running migrations
# add_predefined_data()


# How the above works:
# Steps in the Process:
# 1. When the add_predefined_data() function is called, it populates the database with predefined categories and skills.

# 2. During the user sign-up process, the user is presented with options to select multiple categories and skills.

# 3. Once the user selects their desired categories and skills, those selections are saved in the CustomUser model's categories and skills fields, which are ManyToManyField relationships.

# 4. Django takes care of associating the selected categories and skills with the user in the appropriate join tables.




