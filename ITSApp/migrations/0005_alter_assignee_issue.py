# Generated by Django 3.2.13 on 2022-05-26 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ITSApp', '0004_auto_20220526_1740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignee',
            name='issue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignee', to='ITSApp.issue'),
        ),
    ]
