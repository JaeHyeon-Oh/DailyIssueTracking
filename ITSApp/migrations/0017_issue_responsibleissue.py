# Generated by Django 3.2.13 on 2022-05-31 02:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ITSApp', '0016_alter_issue_deadline'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='responsibleIssue',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='issue', to='ITSApp.responsibleissue'),
            preserve_default=False,
        ),
    ]