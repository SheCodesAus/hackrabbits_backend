# Generated by Django 5.1.5 on 2025-01-24 09:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_userachievement_achievement_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='industry',
            field=models.CharField(blank=True, choices=[('EDUCATION', 'Education'), ('HEALTHCARE', 'Healthcare'), ('CYBER_SECURITY', 'Cyber Security'), ('SOFTWARE_ENGINEERING', 'Software Engineering'), ('DATA_SCIENCE', 'Data Science'), ('FINANCE', 'Finance'), ('AI', 'AI'), ('ENERGY', 'Energy'), ('TRANSPORTATION', 'Transportation'), ('VIDEO_GAME_DEV', 'Video Game Development'), ('GOVERNMENT', 'Government'), ('MEDIA_ENTERTAINMENT', 'Media & Entertainment'), ('STARTUP', 'Startup'), ('NON_PROFIT', 'Non-Profit')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='location',
            field=models.CharField(blank=True, choices=[('PERTH', 'Perth'), ('ADELAIDE', 'Adelaide'), ('MELBOURNE', 'Melbourne'), ('HOBART', 'Hobart'), ('CANBERRA', 'Canberra'), ('SYDNEY', 'Sydney'), ('BRISBANE', 'Brisbane'), ('DARWIN', 'Darwin')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('ADMIN', 'Admin'), ('ROLE_MODEL', 'Role Model'), ('COMMUNITY_USER', 'Community User')], default='COMMUNITY_USER', max_length=20),
        ),
    ]