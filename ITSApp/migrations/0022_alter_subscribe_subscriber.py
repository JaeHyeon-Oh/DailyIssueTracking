# Generated by Django 3.2.13 on 2022-06-09 04:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ITSApp', '0021_project_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscribe',
            name='subscriber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribed_user', to=settings.AUTH_USER_MODEL),
        ),
    ]