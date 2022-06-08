# Generated by Django 3.2.13 on 2022-05-26 08:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ITSApp', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignee',
            name='issue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ITSApp.issue'),
        ),
        migrations.AlterField(
            model_name='assignee',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]