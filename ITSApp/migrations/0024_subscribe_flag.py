# Generated by Django 3.2.13 on 2022-06-13 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ITSApp', '0023_remove_subscribe_flag'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscribe',
            name='flag',
            field=models.BooleanField(default=True),
        ),
    ]
