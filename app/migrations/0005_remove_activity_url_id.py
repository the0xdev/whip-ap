# Generated by Django 4.2.18 on 2025-03-18 02:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_activity_url_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='url_id',
        ),
    ]
