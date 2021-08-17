# Generated by Django 3.2.6 on 2021-08-17 08:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0016_alter_attendee_att_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendee',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attended_events', to=settings.AUTH_USER_MODEL),
        ),
    ]
