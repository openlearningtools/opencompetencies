# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('competencies', '0002_organization_public'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='editors',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='org_editors'),
        ),
    ]
