# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competencies', '0002_auto_20150518_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='competencyarea',
            name='phrase',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
