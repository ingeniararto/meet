# Generated by Django 3.2.6 on 2021-08-19 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0020_event_max_num_of_attendees'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_picture',
            field=models.ImageField(default=None, upload_to='static/uploads/event'),
        ),
    ]
