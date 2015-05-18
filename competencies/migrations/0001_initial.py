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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('competency_area', models.CharField(max_length=500)),
                ('public', models.BooleanField(default=False)),
                ('student_friendly', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='EssentialUnderstanding',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('essential_understanding', models.CharField(max_length=2000)),
                ('public', models.BooleanField(default=False)),
                ('student_friendly', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('competency_area', models.ForeignKey(to='competencies.CompetencyArea')),
            ],
        ),
        migrations.CreateModel(
            name='LearningTarget',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('learning_target', models.CharField(max_length=2000)),
                ('public', models.BooleanField(default=False)),
                ('student_friendly', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('essential_understanding', models.ForeignKey(to='competencies.EssentialUnderstanding')),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level_type', models.CharField(max_length=500, choices=[(b'Apprentice', b'Apprentice'), (b'Technician', b'Technician'), (b'Master', b'Master'), (b'Professional', b'Professional')])),
                ('level_description', models.CharField(max_length=5000)),
                ('public', models.BooleanField(default=False)),
                ('competency_area', models.ForeignKey(to='competencies.CompetencyArea')),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='SubdisciplineArea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subdiscipline_area', models.CharField(max_length=500)),
                ('public', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubjectArea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject_area', models.CharField(max_length=500)),
                ('public', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True)),
                ('school', models.ForeignKey(to='competencies.School')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('schools', models.ManyToManyField(to='competencies.School', blank=True)),
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
            order_with_respect_to='school',
        ),
        migrations.AlterOrderWithRespectTo(
            name='subdisciplinearea',
            order_with_respect_to='subject_area',
        ),
        migrations.AlterUniqueTogether(
            name='level',
            unique_together=set([('competency_area', 'level_type')]),
        ),
        migrations.AlterOrderWithRespectTo(
            name='level',
            order_with_respect_to='competency_area',
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
