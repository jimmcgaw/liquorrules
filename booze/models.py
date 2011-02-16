from django.db import models

from django.utils import simplejson

class DrinkLink(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    href = models.CharField(max_length=200, db_index=True)
    scraped = models.BooleanField(default=False)

class Cocktail(models.Model):
    name = models.CharField(max_length=100)
    summary = models.TextField()
    instructions = models.TextField()
    url = models.ForeignKey("booze.DrinkLink")
    
    def get_json(self):
        data = {}
        data['name'] = self.name
        data['summary'] = self.summary
        data['instructions'] = self.instructions
        ingredients = [ing.get_amount_name() for ing in self.ingredient_set.all()]
        data['ingredients'] = ingredients
        json = simplejson.dumps(data)
        return json

class Ingredient(models.Model):
    amount = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    href = models.CharField(max_length=100, default=u"")
    cocktail = models.ForeignKey('booze.Cocktail')
    
    def get_amount_name(self):
        return self.amount + " " + self.name
    
    def __unicode__(self):
        return self.name
