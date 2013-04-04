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

        # Adding field 'SubjectArea.school'
        db.add_column(u'competencies_subjectarea', 'school',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['competencies.School']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'School'
        db.delete_table(u'competencies_school')

        # Deleting field 'SubjectArea.school'
        db.delete_column(u'competencies_subjectarea', 'school_id')


    models = {
        u'competencies.competencyarea': {
            'Meta': {'object_name': 'CompetencyArea'},
            'competency_area': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subdiscipline_area': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['competencies.SubdisciplineArea']"}),
            'subject_area': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['competencies.SubjectArea']"})
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
