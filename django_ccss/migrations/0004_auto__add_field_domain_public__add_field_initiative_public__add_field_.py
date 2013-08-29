# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Domain.public'
        db.add_column(u'django_ccss_domain', 'public',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Initiative.public'
        db.add_column(u'django_ccss_initiative', 'public',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Standard.public'
        db.add_column(u'django_ccss_standard', 'public',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Component.public'
        db.add_column(u'django_ccss_component', 'public',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Grade.public'
        db.add_column(u'django_ccss_grade', 'public',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Framework.public'
        db.add_column(u'django_ccss_framework', 'public',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Domain.public'
        db.delete_column(u'django_ccss_domain', 'public')

        # Deleting field 'Initiative.public'
        db.delete_column(u'django_ccss_initiative', 'public')

        # Deleting field 'Standard.public'
        db.delete_column(u'django_ccss_standard', 'public')

        # Deleting field 'Component.public'
        db.delete_column(u'django_ccss_component', 'public')

        # Deleting field 'Grade.public'
        db.delete_column(u'django_ccss_grade', 'public')

        # Deleting field 'Framework.public'
        db.delete_column(u'django_ccss_framework', 'public')


    models = {
        u'django_ccss.component': {
            'Meta': {'object_name': 'Component'},
            'component': ('django.db.models.fields.TextField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'dot_notation': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'standard': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_ccss.Standard']"}),
            'student_friendly': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'django_ccss.domain': {
            'Meta': {'object_name': 'Domain'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'dot_notation': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'framework': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_ccss.Framework']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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
            'initiative': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_ccss.Initiative']"}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'django_ccss.grade': {
            'Meta': {'object_name': 'Grade'},
            'dot_notation': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'grade': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'django_ccss.initiative': {
            'Meta': {'object_name': 'Initiative'},
            'dot_notation': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initiative': ('django.db.models.fields.CharField', [], {'default': "'CCSS'", 'max_length': '255'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'django_ccss.set': {
            'Meta': {'object_name': 'Set'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'django_ccss.standard': {
            'Meta': {'object_name': 'Standard'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_ccss.Domain']"}),
            'dot_notation': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'grade': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['django_ccss.Grade']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'standard': ('django.db.models.fields.TextField', [], {}),
            'student_friendly': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['django_ccss']