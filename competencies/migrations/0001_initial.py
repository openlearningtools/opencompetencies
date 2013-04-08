# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'School'
        db.create_table(u'competencies_school', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal(u'competencies', ['School'])

        # Adding model 'SubjectArea'
        db.create_table(u'competencies_subjectarea', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject_area', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competencies.School'])),
        ))
        db.send_create_signal(u'competencies', ['SubjectArea'])

        # Adding model 'SubdisciplineArea'
        db.create_table(u'competencies_subdisciplinearea', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subdiscipline_area', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('subject_area', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competencies.SubjectArea'])),
        ))
        db.send_create_signal(u'competencies', ['SubdisciplineArea'])

        # Adding model 'CompetencyArea'
        db.create_table(u'competencies_competencyarea', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('competency_area', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('subject_area', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['competencies.SubjectArea'], blank=True)),
            ('subdiscipline_area', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['competencies.SubdisciplineArea'], blank=True)),
        ))
        db.send_create_signal(u'competencies', ['CompetencyArea'])

        # Adding model 'EssentialUnderstanding'
        db.create_table(u'competencies_essentialunderstanding', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('essential_understanding', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('competency_area', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competencies.CompetencyArea'])),
        ))
        db.send_create_signal(u'competencies', ['EssentialUnderstanding'])

        # Adding model 'LearningTarget'
        db.create_table(u'competencies_learningtarget', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('learning_target', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('essential_understanding', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competencies.EssentialUnderstanding'])),
        ))
        db.send_create_signal(u'competencies', ['LearningTarget'])


    def backwards(self, orm):
        # Deleting model 'School'
        db.delete_table(u'competencies_school')

        # Deleting model 'SubjectArea'
        db.delete_table(u'competencies_subjectarea')

        # Deleting model 'SubdisciplineArea'
        db.delete_table(u'competencies_subdisciplinearea')

        # Deleting model 'CompetencyArea'
        db.delete_table(u'competencies_competencyarea')

        # Deleting model 'EssentialUnderstanding'
        db.delete_table(u'competencies_essentialunderstanding')

        # Deleting model 'LearningTarget'
        db.delete_table(u'competencies_learningtarget')


    models = {
        u'competencies.competencyarea': {
            'Meta': {'object_name': 'CompetencyArea'},
            'competency_area': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subdiscipline_area': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'to': u"orm['competencies.SubdisciplineArea']", 'blank': 'True'}),
            'subject_area': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'to': u"orm['competencies.SubjectArea']", 'blank': 'True'})
        },
        u'competencies.essentialunderstanding': {
            'Meta': {'object_name': 'EssentialUnderstanding'},
            'competency_area': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['competencies.CompetencyArea']"}),
            'essential_understanding': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'competencies.learningtarget': {
            'Meta': {'object_name': 'LearningTarget'},
            'essential_understanding': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['competencies.EssentialUnderstanding']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'learning_target': ('django.db.models.fields.CharField', [], {'max_length': '2000'})
        },
        u'competencies.school': {
            'Meta': {'object_name': 'School'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'competencies.subdisciplinearea': {
            'Meta': {'object_name': 'SubdisciplineArea'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subdiscipline_area': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'subject_area': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['competencies.SubjectArea']"})
        },
        u'competencies.subjectarea': {
            'Meta': {'object_name': 'SubjectArea'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['competencies.School']"}),
            'subject_area': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        }
    }

    complete_apps = ['competencies']