# Generated by Django 3.2.6 on 2021-08-26 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_remove_profile_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='static/img/product/no_image.png', upload_to='static/uploads/'),
        ),
    ]
