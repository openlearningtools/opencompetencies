# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competencies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='competencyarea',
            name='alias',
            field=models.CharField(max_length=500, default='Graduation Standard'),
        ),
        migrations.AlterField(
            model_name='level',
            name='level_type',
            field=models.CharField(choices=[('Apprentice', 'Apprentice'), ('Technician', 'Technician'), ('Master', 'Master'), ('Professional', 'Professional')], max_length=500),
        ),
    ]
