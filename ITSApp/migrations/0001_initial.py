# Generated by Django 3.2.13 on 2022-05-17 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('attachment_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='Board',
            fields=[
                ('board_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('comment_content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('dept_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('dept_name', models.CharField(choices=[('IT', 'IT실'), ('BN', '경영지원'), ('BR', '브랜드전략'), ('CD', '여신관리')], default='IT', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('issue_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('deadline', models.DateTimeField()),
                ('priority', models.CharField(choices=[('F', '긴급'), ('M', '보통'), ('S', '여유')], default='M', max_length=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('project_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('project_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Responsibility',
            fields=[
                ('Responsibility_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('responsibility_type', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ResponsibleIssue',
            fields=[
                ('responsible_issue_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('responsible_issue_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Subscribe',
            fields=[
                ('subscribe_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('username', models.CharField(max_length=40, primary_key=True, serialize=False, unique=True)),
                ('key', models.CharField(max_length=40, unique=True)),
            ],
        ),
    ]
