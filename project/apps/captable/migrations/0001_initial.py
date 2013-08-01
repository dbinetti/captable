# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Investor'
        db.create_table(u'captable_investor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('contact', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
        ))
        db.send_create_signal(u'captable', ['Investor'])

        # Adding model 'Shareholder'
        db.create_table(u'captable_shareholder', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('investor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['captable.Investor'])),
        ))
        db.send_create_signal(u'captable', ['Shareholder'])

        # Adding model 'Security'
        db.create_table(u'captable_security', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('security_type', self.gf('django.db.models.fields.IntegerField')(max_length=20)),
            ('conversion_ratio', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('liquidation_preference', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('is_participating', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('participation_cap', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('price_per_share', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('price_cap', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('discount_rate', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('interest_rate', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('default_conversion_price', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('pre', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('seniority', self.gf('django.db.models.fields.IntegerField')(default=1, blank=True)),
            ('conversion_security', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['captable.Security'], null=True, blank=True)),
        ))
        db.send_create_signal(u'captable', ['Security'])

        # Adding model 'Addition'
        db.create_table(u'captable_addition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('authorized', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('security', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['captable.Security'], null=True, blank=True)),
        ))
        db.send_create_signal(u'captable', ['Addition'])

        # Adding model 'Certificate'
        db.create_table(u'captable_certificate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('shares', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('returned', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('cash', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('refunded', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('debt', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('forgiven', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('granted', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('exercised', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('cancelled', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_prorata', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('vesting_start', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('vesting_stop', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('vesting_term', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('vesting_cliff', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('vesting_immediate', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('vested_direct', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('vesting_trigger', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('expiration_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('converted_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('security', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['captable.Security'])),
            ('shareholder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['captable.Shareholder'])),
        ))
        db.send_create_signal(u'captable', ['Certificate'])

        # Adding model 'Transaction'
        db.create_table(u'captable_transaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('certificate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['captable.Certificate'])),
        ))
        db.send_create_signal(u'captable', ['Transaction'])


    def backwards(self, orm):
        # Deleting model 'Investor'
        db.delete_table(u'captable_investor')

        # Deleting model 'Shareholder'
        db.delete_table(u'captable_shareholder')

        # Deleting model 'Security'
        db.delete_table(u'captable_security')

        # Deleting model 'Addition'
        db.delete_table(u'captable_addition')

        # Deleting model 'Certificate'
        db.delete_table(u'captable_certificate')

        # Deleting model 'Transaction'
        db.delete_table(u'captable_transaction')


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
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'debt': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'exercised': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'forgiven': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'granted': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_prorata': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
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
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        u'captable.security': {
            'Meta': {'ordering': "['date']", 'object_name': 'Security'},
            'conversion_ratio': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'conversion_security': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['captable.Security']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'default_conversion_price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
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
        },
        u'captable.transaction': {
            'Meta': {'ordering': "['date']", 'object_name': 'Transaction'},
            'certificate': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['captable.Certificate']"}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['captable']