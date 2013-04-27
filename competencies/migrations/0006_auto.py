# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field competency_areas on 'Pathway'
        db.create_table(u'competencies_pathway_competency_areas', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pathway', models.ForeignKey(orm[u'competencies.pathway'], null=False)),
            ('competencyarea', models.ForeignKey(orm[u'competencies.competencyarea'], null=False))
        ))
        db.create_unique(u'competencies_pathway_competency_areas', ['pathway_id', 'competencyarea_id'])


    def backwards(self, orm):
        # Removing M2M table for field competency_areas on 'Pathway'
        db.delete_table('competencies_pathway_competency_areas')


    models = {
        u'competencies.competencyarea': {
            'Meta': {'object_name': 'CompetencyArea'},
            'competency_area': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subdiscipline_area': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['competencies.SubdisciplineArea']", 'null': 'True', 'blank': 'True'}),
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
        u'competencies.pathway': {
            'Meta': {'object_name': 'Pathway'},
            'competency_areas': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['competencies.CompetencyArea']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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