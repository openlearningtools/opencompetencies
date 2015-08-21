# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competencies', '0003_organization_editors'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='organizations',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='subject_areas',
        ),
    ]
