# Generated by Django 3.2.6 on 2021-08-17 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='photo',
            field=models.TextField(default=None),
        ),
    ]
