# Generated by Django 3.2.6 on 2021-08-19 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_profile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(default=None, upload_to='static/uploads/'),
        ),
    ]
