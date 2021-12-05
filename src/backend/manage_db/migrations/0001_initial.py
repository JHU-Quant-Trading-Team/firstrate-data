# Generated by Django 3.2.9 on 2021-12-05 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('ticker', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('last_updated', models.DateTimeField()),
                ('file_path', models.CharField(default='', max_length=256)),
                ('download_link', models.CharField(default='', max_length=256)),
                ('update_link', models.CharField(default='', max_length=256)),
            ],
        ),
    ]
