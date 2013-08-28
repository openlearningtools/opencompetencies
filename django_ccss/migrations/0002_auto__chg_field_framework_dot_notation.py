# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Framework.dot_notation'
        db.alter_column(u'django_ccss_framework', 'dot_notation', self.gf('django.db.models.fields.CharField')(max_length=255))

    def backwards(self, orm):

        # Changing field 'Framework.dot_notation'
        db.alter_column(u'django_ccss_framework', 'dot_notation', self.gf('django.db.models.fields.CharField')(max_length=10))

    models = {
        u'django_ccss.component': {
            'Meta': {'object_name': 'Component'},
            'component': ('django.db.models.fields.TextField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'dot_notation': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'standard': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_ccss.Standard']"}),
            'student_friendly': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'django_ccss.domain': {
            'Meta': {'object_name': 'Domain'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'default': "'W'", 'max_length': '255'}),
            'dot_notation': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'framework': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_ccss.Framework']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'django_ccss.elaelement': {
            'Meta': {'object_name': 'ELAElement'},
            'component': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_ccss.Component']", 'null': 'True', 'blank': 'True'}),
            'dot_notation': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'django_ccss.framework': {
            'Meta': {'object_name': 'Framework'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'dot_notation': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'framework': ('django.db.models.fields.CharField', [], {'default': "'ELA_LIT'", 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initiative': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_ccss.Initiative']"})
        },
        u'django_ccss.grade': {
            'Meta': {'object_name': 'Grade'},
            'dot_notation': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'grade': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'django_ccss.initiative': {
            'Meta': {'object_name': 'Initiative'},
            'dot_notation': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initiative': ('django.db.models.fields.CharField', [], {'default': "'CCSS'", 'max_length': '255'})
        },
        u'django_ccss.set': {
            'Meta': {'object_name': 'Set'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'django_ccss.standard': {
            'Meta': {'object_name': 'Standard'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_ccss.Domain']"}),
            'dot_notation': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'grade': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['django_ccss.Grade']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'standard': ('django.db.models.fields.TextField', [], {}),
            'student_friendly': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['django_ccss']