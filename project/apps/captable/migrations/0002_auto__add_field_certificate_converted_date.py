# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Certificate.converted_date'
        db.add_column(u'captable_certificate', 'converted_date',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Certificate.converted_date'
        db.delete_column(u'captable_certificate', 'converted_date')


    models = {
        u'captable.addition': {
            'Meta': {'ordering': "['date']", 'object_name': 'Addition'},
            'authorized': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'security': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['captable.Security']", 'null': 'True', 'blank': 'True'})
        },
        u'captable.certificate': {
            'Meta': {'ordering': "['name']", 'object_name': 'Certificate'},
            'cancelled': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'cash': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'converted_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'exercised': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'forgiven': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'granted': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_prorata': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'principal': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'refunded': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'returned': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'security': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['captable.Security']"}),
            'shareholder': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['captable.Shareholder']"}),
            'shares': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'vested_direct': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'vesting_cliff': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'vesting_immediate': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'vesting_start': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'vesting_stop': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'vesting_term': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'vesting_trigger': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'captable.investor': {
            'Meta': {'ordering': "['name']", 'object_name': 'Investor'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        u'captable.security': {
            'Meta': {'ordering': "['date']", 'object_name': 'Security'},
            'conversion_ratio': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'discount_rate': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interest_rate': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'is_participating': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'liquidation_preference': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'participation_cap': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'pre': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'price_cap': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'price_per_share': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'security_type': ('django.db.models.fields.IntegerField', [], {'max_length': '20'}),
            'seniority': ('django.db.models.fields.IntegerField', [], {'default': '1', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'captable.shareholder': {
            'Meta': {'ordering': "['name']", 'object_name': 'Shareholder'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'investor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['captable.Investor']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['captable']