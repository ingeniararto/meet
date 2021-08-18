# Generated by Django 3.2.6 on 2021-08-18 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_alter_profile_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followed_profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='accounts.profile')),
                ('follower', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='followed_profiles', to='accounts.profile')),
            ],
        ),
    ]
