# Generated by Django 3.2.13 on 2022-05-27 07:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ITSApp', '0012_subscribe_issue'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscribe',
            old_name='subscribe_id',
            new_name='id',
        ),
    ]
