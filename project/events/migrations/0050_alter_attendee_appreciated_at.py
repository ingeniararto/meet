# Generated by Django 3.2.6 on 2021-09-08 11:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0049_alter_attendee_appreciated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendee',
            name='appreciated_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 8, 14, 17, 4, 5993), null=True),
        ),
    ]
