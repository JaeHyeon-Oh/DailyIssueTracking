# Generated by Django 3.2.13 on 2022-06-03 02:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ITSApp', '0017_issue_responsibleissue'),
    ]

    operations = [
        migrations.RenameField(
            model_name='board',
            old_name='title',
            new_name='state',
        ),
    ]
