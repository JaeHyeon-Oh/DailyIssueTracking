# Generated by Django 3.2.13 on 2022-05-27 00:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ITSApp', '0008_alter_issue_reporter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignee',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignee', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='issue',
            name='reporter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issue', to=settings.AUTH_USER_MODEL),
        ),
    ]