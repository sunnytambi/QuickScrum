# -*- coding: utf-8 -*-
# Generated by Django 1.10b1 on 2016-06-28 09:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20160628_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status_jiraissue',
            name='jira_issue_id',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='status_jiraissue',
            name='jira_issue_text',
            field=models.TextField(default=''),
        ),
    ]
