# Generated by Django 3.2.13 on 2022-06-14 05:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ITSApp', '0024_subscribe_flag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='responsibility',
            name='responsible_issue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsibility', to='ITSApp.responsibleissue'),
        ),
    ]
