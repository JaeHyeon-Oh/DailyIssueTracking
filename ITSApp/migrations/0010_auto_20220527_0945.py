# Generated by Django 3.2.13 on 2022-05-27 00:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ITSApp', '0009_auto_20220527_0942'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='user',
        ),
        migrations.RemoveField(
            model_name='subscribe',
            name='user',
        ),
        migrations.AddField(
            model_name='comment',
            name='writer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='ITSJwt.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscribe',
            name='subscriber',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='subscribe', to='ITSJwt.user'),
            preserve_default=False,
        ),
    ]