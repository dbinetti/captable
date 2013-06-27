# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Company'
        db.create_table(u'captable_company', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
        ))
        db.send_create_signal(u'captable', ['Company'])

        # Adding M2M table for field owner on 'Company'
        m2m_table_name = db.shorten_name(u'captable_company_owner')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('company', models.ForeignKey(orm[u'captable.company'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['company_id', 'user_id'])

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
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
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
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['captable.Company'])),
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
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=1, null=True, blank=True)),
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
            ('is_vested', self.gf('django.db.models.fields.BooleanField')(default=False)),
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
        # Deleting model 'Company'
        db.delete_table(u'captable_company')

        # Removing M2M table for field owner on 'Company'
        db.delete_table(db.shorten_name(u'captable_company_owner'))

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
            'is_vested': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'refunded': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'returned': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'security': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['captable.Security']"}),
            'shareholder': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['captable.Shareholder']"}),
            'shares': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'vested_direct': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'vesting_cliff': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'vesting_immediate': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'vesting_start': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'vesting_stop': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'vesting_term': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'vesting_trigger': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'captable.company': {
            'Meta': {'ordering': "['name']", 'object_name': 'Company'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'owner': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
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
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['captable.Company']"}),
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
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
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
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['captable']