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
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('public', models.BooleanField(default=False)),
                ('student_friendly', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('graduation_standard', models.CharField(max_length=500)),
                ('phrase', models.CharField(blank=True, max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='LearningObjective',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('public', models.BooleanField(default=False)),
                ('student_friendly', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('learning_objective', models.CharField(max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('org_type', models.CharField(max_length=500, default='school')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PerformanceIndicator',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('public', models.BooleanField(default=False)),
                ('student_friendly', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('performance_indicator', models.CharField(max_length=2000)),
                ('graduation_standard', models.ForeignKey(to='competencies.GraduationStandard')),
            ],
        ),
        migrations.CreateModel(
            name='SubdisciplineArea',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('public', models.BooleanField(default=False)),
                ('student_friendly', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('subdiscipline_area', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='SubjectArea',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
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
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('organizations', models.ManyToManyField(blank=True, to='competencies.Organization')),
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
            field=models.ForeignKey(blank=True, to='competencies.SubdisciplineArea', null=True),
        ),
        migrations.AddField(
            model_name='graduationstandard',
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
        migrations.AlterOrderWithRespectTo(
            name='performanceindicator',
            order_with_respect_to='graduation_standard',
        ),
        migrations.AlterUniqueTogether(
            name='organization',
            unique_together=set([('name', 'owner')]),
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
