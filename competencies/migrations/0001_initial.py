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
            name='GraduationStandard',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('graduation_standard', models.CharField(max_length=500)),
                ('public', models.BooleanField(default=False)),
                ('student_friendly', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('alias', models.CharField(max_length=500, default='Graduation Standard')),
                ('phrase', models.CharField(blank=True, max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='LearningObjective',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('learning_objective', models.CharField(max_length=2000)),
                ('public', models.BooleanField(default=False)),
                ('student_friendly', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('level_type', models.CharField(max_length=500, choices=[('Apprentice', 'Apprentice'), ('Technician', 'Technician'), ('Master', 'Master'), ('Professional', 'Professional')])),
                ('level_description', models.CharField(max_length=5000)),
                ('public', models.BooleanField(default=False)),
                ('graduation_standard', models.ForeignKey(to='competencies.GraduationStandard')),
            ],
        ),
        migrations.CreateModel(
            name='PerformanceIndicator',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('performance_indicator', models.CharField(max_length=2000)),
                ('public', models.BooleanField(default=False)),
                ('student_friendly', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('graduation_standard', models.ForeignKey(to='competencies.GraduationStandard')),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='SubdisciplineArea',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('subdiscipline_area', models.CharField(max_length=500)),
                ('public', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubjectArea',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('subject_area', models.CharField(max_length=500)),
                ('public', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True)),
                ('school', models.ForeignKey(to='competencies.School')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('schools', models.ManyToManyField(blank=True, to='competencies.School')),
                ('subject_areas', models.ManyToManyField(blank=True, to='competencies.SubjectArea')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='subdisciplinearea',
            name='subject_area',
            field=models.ForeignKey(to='competencies.SubjectArea'),
        ),
        migrations.AddField(
            model_name='learningobjective',
            name='performance_indicator',
            field=models.ForeignKey(to='competencies.PerformanceIndicator'),
        ),
        migrations.AddField(
            model_name='graduationstandard',
            name='subdiscipline_area',
            field=models.ForeignKey(to='competencies.SubdisciplineArea', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='graduationstandard',
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
        migrations.AlterOrderWithRespectTo(
            name='performanceindicator',
            order_with_respect_to='graduation_standard',
        ),
        migrations.AlterUniqueTogether(
            name='level',
            unique_together=set([('graduation_standard', 'level_type')]),
        ),
        migrations.AlterOrderWithRespectTo(
            name='level',
            order_with_respect_to='graduation_standard',
        ),
        migrations.AlterOrderWithRespectTo(
            name='learningobjective',
            order_with_respect_to='performance_indicator',
        ),
        migrations.AlterOrderWithRespectTo(
            name='graduationstandard',
            order_with_respect_to='subject_area',
        ),
    ]
