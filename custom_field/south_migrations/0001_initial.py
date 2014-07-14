# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CustomField'
        db.create_table('custom_field_customfield', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('field_type', self.gf('django.db.models.fields.CharField')(default='t', max_length=1)),
        ))
        db.send_create_signal('custom_field', ['CustomField'])

        # Adding unique constraint on 'CustomField', fields ['name', 'content_type']
        db.create_unique('custom_field_customfield', ['name', 'content_type_id'])

        # Adding model 'CustomFieldValue'
        db.create_table('custom_field_customfieldvalue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('field', self.gf('django.db.models.fields.related.ForeignKey')(related_name='instance', to=orm['custom_field.CustomField'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True, blank=True)),
        ))
        db.send_create_signal('custom_field', ['CustomFieldValue'])

        # Adding unique constraint on 'CustomFieldValue', fields ['field', 'object_id']
        db.create_unique('custom_field_customfieldvalue', ['field_id', 'object_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'CustomFieldValue', fields ['field', 'object_id']
        db.delete_unique('custom_field_customfieldvalue', ['field_id', 'object_id'])

        # Removing unique constraint on 'CustomField', fields ['name', 'content_type']
        db.delete_unique('custom_field_customfield', ['name', 'content_type_id'])

        # Deleting model 'CustomField'
        db.delete_table('custom_field_customfield')

        # Deleting model 'CustomFieldValue'
        db.delete_table('custom_field_customfieldvalue')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'custom_field.customfield': {
            'Meta': {'unique_together': "(('name', 'content_type'),)", 'object_name': 'CustomField'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'field_type': ('django.db.models.fields.CharField', [], {'default': "'t'", 'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '75'})
        },
        'custom_field.customfieldvalue': {
            'Meta': {'unique_together': "(('field', 'object_id'),)", 'object_name': 'CustomFieldValue'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'field': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'instance'", 'to': "orm['custom_field.CustomField']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['custom_field']