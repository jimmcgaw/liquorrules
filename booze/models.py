from django.db import models
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Q
from django.utils import simplejson

import operator

DRINKS_PER_PAGE = 50

class DrinkLink(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    href = models.CharField(max_length=200, db_index=True)
    scraped = models.BooleanField(default=False)

class CocktailManager(models.Manager):
    def search(self, query, page):
        try:
            page = int(page)
        except ValueError:
            page = 1
        
        terms = [term.strip() for term in query.split()]
        q_objects = []
        
        for term in terms:
            q_objects.append(Q(name__icontains=term))
            q_objects.append(Q(ingredient__name__icontains=term))
            #q_objects.append(Q(description__icontains=term))
            
        if terms:
            qs = self.get_query_set().filter(reduce(operator.or_, q_objects))
        else:
            qs = self.get_query_set()
        
        paginator = Paginator(qs, DRINKS_PER_PAGE)
        
        try:
            results = paginator.page(page).object_list
        except (InvalidPage, EmptyPage):
            results = paginator.page(1).object_list

        return results, paginator

class Cocktail(models.Model):
    name = models.CharField(max_length=100)
    summary = models.TextField()
    instructions = models.TextField()
    url = models.ForeignKey("booze.DrinkLink")
    
    objects = CocktailManager()
    
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


class IngredientUrl(models.Model):
    href = models.CharField(max_length=100)
    
class IngredientChild(models.Model):
    parent = models.ForeignKey("booze.IngredientUrl")
    href = models.CharField(max_length=100)
    
class LiquorChild(models.Model):
    parent = models.ForeignKey("booze.IngredientUrl")
    href = models.CharField(max_length=100)