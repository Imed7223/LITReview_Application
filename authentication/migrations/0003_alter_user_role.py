# Generated by Django 5.0.1 on 2025-06-03 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_alter_user_profile_photo_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(default='user', max_length=30),
        ),
    ]
