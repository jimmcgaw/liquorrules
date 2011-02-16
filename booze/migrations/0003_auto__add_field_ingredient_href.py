# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Ingredient.href'
        db.add_column('booze_ingredient', 'href', self.gf('django.db.models.fields.CharField')(default=u'', max_length=100), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Ingredient.href'
        db.delete_column('booze_ingredient', 'href')


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
            'href': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'scraped': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'booze.ingredient': {
            'Meta': {'object_name': 'Ingredient'},
            'amount': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'cocktail': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['booze.Cocktail']"}),
            'href': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['booze']
