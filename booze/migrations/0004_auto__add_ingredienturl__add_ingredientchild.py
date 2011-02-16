# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'IngredientUrl'
        db.create_table('booze_ingredienturl', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('href', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('booze', ['IngredientUrl'])

        # Adding model 'IngredientChild'
        db.create_table('booze_ingredientchild', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['booze.IngredientUrl'])),
            ('href', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('booze', ['IngredientChild'])


    def backwards(self, orm):
        
        # Deleting model 'IngredientUrl'
        db.delete_table('booze_ingredienturl')

        # Deleting model 'IngredientChild'
        db.delete_table('booze_ingredientchild')


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
        },
        'booze.ingredientchild': {
            'Meta': {'object_name': 'IngredientChild'},
            'href': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['booze.IngredientUrl']"})
        },
        'booze.ingredienturl': {
            'Meta': {'object_name': 'IngredientUrl'},
            'href': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['booze']
