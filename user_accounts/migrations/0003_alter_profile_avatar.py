# Generated by Django 5.1.7 on 2025-03-26 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_accounts', '0002_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.CharField(default='avatar9.png', max_length=100),
        ),
    ]
