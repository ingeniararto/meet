# Generated by Django 3.2.6 on 2021-09-06 11:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0046_alter_attendee_appreciated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendee',
            name='appreciated_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 6, 14, 18, 39, 818351), null=True),
        ),
    ]
