# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'LearningTarget.student_friendly'
        db.add_column(u'competencies_learningtarget', 'student_friendly',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'LearningTarget.student_friendly'
        db.delete_column(u'competencies_learningtarget', 'student_friendly')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'competencies.competencyarea': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'CompetencyArea'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'competency_area': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subdiscipline_area': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['competencies.SubdisciplineArea']", 'null': 'True', 'blank': 'True'}),
            'subject_area': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['competencies.SubjectArea']"})
        },
        u'competencies.essentialunderstanding': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'EssentialUnderstanding'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'competency_area': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['competencies.CompetencyArea']"}),
            'essential_understanding': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'competencies.learningtarget': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'LearningTarget'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'essential_understanding': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['competencies.EssentialUnderstanding']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'learning_target': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'student_friendly': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'competencies.level': {
            'Meta': {'ordering': "(u'_order',)", 'unique_together': "(('competency_area', 'level_type'),)", 'object_name': 'Level'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'competency_area': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['competencies.CompetencyArea']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level_description': ('django.db.models.fields.CharField', [], {'max_length': '5000'}),
            'level_type': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'competencies.pathway': {
            'Meta': {'object_name': 'Pathway'},
            'competency_areas': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['competencies.CompetencyArea']", 'null': 'True', 'blank': 'True'}),
            'essential_understandings': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['competencies.EssentialUnderstanding']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'learning_targets': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['competencies.LearningTarget']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subdiscipline_area': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'subject_area': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['competencies.SubjectArea']"})
        },
        u'competencies.subjectarea': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'SubjectArea'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['competencies.School']"}),
            'subject_area': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'competencies.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pathways': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['competencies.Pathway']", 'null': 'True', 'blank': 'True'}),
            'schools': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['competencies.School']", 'null': 'True', 'blank': 'True'}),
            'subject_areas': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['competencies.SubjectArea']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['competencies']