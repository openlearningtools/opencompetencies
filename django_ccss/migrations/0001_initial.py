# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Initiative'
        db.create_table(u'django_ccss_initiative', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dot_notation', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('initiative', self.gf('django.db.models.fields.CharField')(default='CCSS', max_length=255)),
        ))
        db.send_create_signal(u'django_ccss', ['Initiative'])

        # Adding model 'Framework'
        db.create_table(u'django_ccss_framework', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('initiative', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_ccss.Initiative'])),
            ('dot_notation', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('framework', self.gf('django.db.models.fields.CharField')(default='ELA_LIT', max_length=255)),
        ))
        db.send_create_signal(u'django_ccss', ['Framework'])

        # Adding model 'Set'
        db.create_table(u'django_ccss_set', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'django_ccss', ['Set'])

        # Adding model 'Domain'
        db.create_table(u'django_ccss_domain', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('framework', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_ccss.Framework'])),
            ('dot_notation', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('domain', self.gf('django.db.models.fields.CharField')(default='W', max_length=255)),
        ))
        db.send_create_signal(u'django_ccss', ['Domain'])

        # Adding model 'Grade'
        db.create_table(u'django_ccss_grade', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('grade', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('dot_notation', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'django_ccss', ['Grade'])

        # Adding model 'Standard'
        db.create_table(u'django_ccss_standard', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('standard', self.gf('django.db.models.fields.TextField')()),
            ('domain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_ccss.Domain'])),
            ('dot_notation', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('student_friendly', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'django_ccss', ['Standard'])

        # Adding M2M table for field grade on 'Standard'
        db.create_table(u'django_ccss_standard_grade', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('standard', models.ForeignKey(orm[u'django_ccss.standard'], null=False)),
            ('grade', models.ForeignKey(orm[u'django_ccss.grade'], null=False))
        ))
        db.create_unique(u'django_ccss_standard_grade', ['standard_id', 'grade_id'])

        # Adding model 'Component'
        db.create_table(u'django_ccss_component', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('component', self.gf('django.db.models.fields.TextField')()),
            ('standard', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_ccss.Standard'])),
            ('dot_notation', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('student_friendly', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'django_ccss', ['Component'])

        # Adding model 'ELAElement'
        db.create_table(u'django_ccss_elaelement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('component', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_ccss.Component'], null=True, blank=True)),
            ('dot_notation', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'django_ccss', ['ELAElement'])


    def backwards(self, orm):
        # Deleting model 'Initiative'
        db.delete_table(u'django_ccss_initiative')

        # Deleting model 'Framework'
        db.delete_table(u'django_ccss_framework')

        # Deleting model 'Set'
        db.delete_table(u'django_ccss_set')

        # Deleting model 'Domain'
        db.delete_table(u'django_ccss_domain')

        # Deleting model 'Grade'
        db.delete_table(u'django_ccss_grade')

        # Deleting model 'Standard'
        db.delete_table(u'django_ccss_standard')

        # Removing M2M table for field grade on 'Standard'
        db.delete_table('django_ccss_standard_grade')

        # Deleting model 'Component'
        db.delete_table(u'django_ccss_component')

        # Deleting model 'ELAElement'
        db.delete_table(u'django_ccss_elaelement')


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
            'dot_notation': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
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