# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CompetencyArea',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('public', models.BooleanField(default=False)),
                ('student_friendly', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('competency_area', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='EssentialUnderstanding',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('public', models.BooleanField(default=False)),
                ('student_friendly', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('essential_understanding', models.CharField(max_length=2000)),
                ('competency_area', models.ForeignKey(to='competencies.CompetencyArea')),
            ],
        ),
        migrations.CreateModel(
            name='LearningTarget',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('public', models.BooleanField(default=False)),
                ('student_friendly', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('learning_target', models.CharField(max_length=2000)),
                ('essential_understanding', models.ForeignKey(to='competencies.EssentialUnderstanding')),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=500)),
                ('org_type', models.CharField(max_length=500, default='school')),
                ('alias_sa', models.CharField(max_length=500, default='subject area')),
                ('alias_sda', models.CharField(max_length=500, default='subdiscipline area')),
                ('alias_ca', models.CharField(max_length=500, default='competency area')),
                ('alias_eu', models.CharField(max_length=500, default='essential understanding')),
                ('alias_lt', models.CharField(max_length=500, default='learning target')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SubdisciplineArea',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('public', models.BooleanField(default=False)),
                ('student_friendly', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('subdiscipline_area', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='SubjectArea',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('public', models.BooleanField(default=False)),
                ('student_friendly', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('subject_area', models.CharField(max_length=500)),
                ('organization', models.ForeignKey(to='competencies.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('organizations', models.ManyToManyField(to='competencies.Organization', blank=True)),
                ('subject_areas', models.ManyToManyField(to='competencies.SubjectArea', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='subdisciplinearea',
            name='subject_area',
            field=models.ForeignKey(to='competencies.SubjectArea'),
        ),
        migrations.AddField(
            model_name='competencyarea',
            name='subdiscipline_area',
            field=models.ForeignKey(blank=True, to='competencies.SubdisciplineArea', null=True),
        ),
        migrations.AddField(
            model_name='competencyarea',
            name='subject_area',
            field=models.ForeignKey(to='competencies.SubjectArea'),
        ),
        migrations.AlterOrderWithRespectTo(
            name='subjectarea',
            order_with_respect_to='organization',
        ),
        migrations.AlterOrderWithRespectTo(
            name='subdisciplinearea',
            order_with_respect_to='subject_area',
        ),
        migrations.AlterUniqueTogether(
            name='organization',
            unique_together=set([('name', 'owner')]),
        ),
        migrations.AlterOrderWithRespectTo(
            name='learningtarget',
            order_with_respect_to='essential_understanding',
        ),
        migrations.AlterOrderWithRespectTo(
            name='essentialunderstanding',
            order_with_respect_to='competency_area',
        ),
        migrations.AlterOrderWithRespectTo(
            name='competencyarea',
            order_with_respect_to='subject_area',
        ),
    ]
