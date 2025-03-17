# SPDX-FileCopyrightText: 2025 Imran M <imran@imranmustafa.net>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# Generated by Django 4.2.18 on 2025-03-09 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_object_publisheddate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='object',
            name='tomb',
            field=models.BooleanField(default=False),
        ),
    ]
