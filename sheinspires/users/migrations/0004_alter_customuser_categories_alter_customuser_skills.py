# Generated by Django 5.1.5 on 2025-01-24 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_customuser_industry_alter_customuser_location_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='categories',
            field=models.ManyToManyField(blank=True, null=True, to='users.category'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='skills',
            field=models.ManyToManyField(blank=True, null=True, to='users.skill'),
        ),
    ]
