# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'LearningTarget.public'
        db.add_column(u'competencies_learningtarget', 'public',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'LearningTarget.public'
        db.delete_column(u'competencies_learningtarget', 'public')


    models = {
        u'competencies.competencyarea': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'CompetencyArea'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'competency_area': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subdiscipline_area': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['competencies.SubdisciplineArea']", 'null': 'True', 'blank': 'True'}),
            'subject_area': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['competencies.SubjectArea']"})
        },
        u'competencies.essentialunderstanding': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'EssentialUnderstanding'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'competency_area': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['competencies.CompetencyArea']"}),
            'essential_understanding': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'competencies.learningtarget': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'LearningTarget'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'essential_understanding': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['competencies.EssentialUnderstanding']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'learning_target': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'competencies.level': {
            'Meta': {'ordering': "(u'_order',)", 'unique_together': "(('competency_area', 'level_type'),)", 'object_name': 'Level'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'competency_area': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['competencies.CompetencyArea']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level_description': ('django.db.models.fields.CharField', [], {'max_length': '5000'}),
            'level_type': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'competencies.pathway': {
            'Meta': {'object_name': 'Pathway'},
            'competency_areas': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['competencies.CompetencyArea']", 'null': 'True', 'blank': 'True'}),
            'essential_understandings': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['competencies.EssentialUnderstanding']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'learning_targets': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['competencies.LearningTarget']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['competencies.School']"}),
            'subdiscipline_areas': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['competencies.SubdisciplineArea']", 'null': 'True', 'blank': 'True'}),
            'subject_areas': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['competencies.SubjectArea']", 'symmetrical': 'False'})
        },
        u'competencies.school': {
            'Meta': {'object_name': 'School'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'competencies.subdisciplinearea': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'SubdisciplineArea'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subdiscipline_area': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'subject_area': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['competencies.SubjectArea']"})
        },
        u'competencies.subjectarea': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'SubjectArea'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['competencies.School']"}),
            'subject_area': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        }
    }

    complete_apps = ['competencies']