# Generated by Django 3.2.6 on 2021-08-17 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_auto_20210816_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendee',
            name='att_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
