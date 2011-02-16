# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'DrinkLink'
        db.create_table('booze_drinklink', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('href', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('scraped', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('booze', ['DrinkLink'])

        # Adding model 'Cocktail'
        db.create_table('booze_cocktail', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('summary', self.gf('django.db.models.fields.TextField')()),
            ('instructions', self.gf('django.db.models.fields.TextField')()),
            ('url', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['booze.DrinkLink'])),
        ))
        db.send_create_signal('booze', ['Cocktail'])

        # Adding model 'Ingredient'
        db.create_table('booze_ingredient', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('amount', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('cocktail', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['booze.Cocktail'])),
        ))
        db.send_create_signal('booze', ['Ingredient'])


    def backwards(self, orm):
        
        # Deleting model 'DrinkLink'
        db.delete_table('booze_drinklink')

        # Deleting model 'Cocktail'
        db.delete_table('booze_cocktail')

        # Deleting model 'Ingredient'
        db.delete_table('booze_ingredient')


    models = {
        'booze.cocktail': {
            'Meta': {'object_name': 'Cocktail'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructions': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'summary': ('django.db.models.fields.TextField', [], {}),
            'url': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['booze.DrinkLink']"})
        },
        'booze.drinklink': {
            'Meta': {'object_name': 'DrinkLink'},
            'href': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'scraped': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'booze.ingredient': {
            'Meta': {'object_name': 'Ingredient'},
            'amount': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'cocktail': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['booze.Cocktail']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['booze']
