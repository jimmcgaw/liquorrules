from BeautifulSoup import BeautifulSoup
from booze.models import DrinkLink, Cocktail, Ingredient, IngredientUrl, IngredientChild, LiquorChild

import urllib2
import re

BASE_URL = 'http://www.drinksmixer.com'

def get_drink_links():
    for num in range(28):
        url = 'http://www.drinksmixer.com/cat/3/%d/' % num
        soup = BeautifulSoup(urllib2.urlopen(url).read())
        parse_drink_links(soup)


def parse_drink_links(soup):
    drinklinks = [link for link in soup('div', {'class':'clr'})[0]('a', href=re.compile(r"^/drink"))]
    for link in drinklinks:
        href = BASE_URL + link['href']
        name = link.renderContents()
        #print "Saving %s at %s" % (name, href)
        DrinkLink.objects.get_or_create(href=href, name=name)


def get_drinks():
    dls = DrinkLink.objects.filter(cocktail=None)
    for dl in dls:
        try:
            print "Getting drink %s" % unicode(dl.name)
        except:
            pass
        url = dl.href
        soup = BeautifulSoup(urllib2.urlopen(url).read())
        summary = directions = u''
        try:
            summary = soup('div',{'property':'v:summary'})[0].renderContents()
        except:
            pass

        try:
            directions = soup('div',{'property':'v:instructions'})[0].renderContents()
        except:
            pass

        c = Cocktail()
        c.name = dl.name
        c.summary = summary
        c.instructions = directions
        c.url = dl
        c.save()

        try:
            recipe = soup('div', {'typeof':'v:Recipe'})[0]
            amounts = recipe('span', {'property':'v:amount'})
            names = recipe('span', {'property':'v:name'})
            for i in range(len(amounts)):
                amount = amounts[i].findAll(text=True)[0]
                name = names[i].findAll(text=True)[0]
                links = names[i]('a')
                if links:
                    link = links[0]['href']
                else:
                    link = u''
                ingredient = Ingredient()
                ingredient.name = name
                ingredient.amount = amount
                ingredient.href = link
                ingredient.cocktail = c
                ingredient.save()
        except:
            pass


def build_hierarchy():
    base_url = "http://www.drinksmixer.com"
    links = IngredientUrl.objects.all()
    for link in links:
        url = base_url + link.href
        print "Getting URL: %s" % url
        soup = BeautifulSoup(urllib2.urlopen(url).read())
        soup = soup('div', {'class':'scat'})
        if soup:
            soup = soup[0]
            child_hrefs = [l['href'] for l in soup('a', href=re.compile("^/desc"))]
            for child in child_hrefs:
                try:
                    ic = IngredientChild()
                    ic.parent = link
                    ic.href = child
                    ic.save()
                    print "Saved child: %s" % child
                except:
                    pass
                
def build_liquor_hierarchy():
    base_url = "http://www.drinksmixer.com"
    links = IngredientUrl.objects.all()
    for link in links:
        url = base_url + link.href
        print "Getting URL: %s" % url
        soup = BeautifulSoup(urllib2.urlopen(url).read())
        soup = soup('p', {'class':'l1a'})
        if soup:
            soup = soup[0]
            child_hrefs = [l['href'] for l in soup('a', href=re.compile("^/desc"))]
            for child in child_hrefs:
                try:
                    ic = LiquorChild()
                    ic.parent = link
                    ic.href = child
                    ic.save()
                    print "Saved child: %s" % child
                except:
                    pass

def get_ing_details():
    links = []
    start_url = "http://www.drinksmixer.com/desca.html"
    links = links + get_page_links(start_url)
    for link in links:
        print link
        
def get_drink_details(link):
    soup = BeautifulSoup(urllib2.urlopen(url).read())
    
        
def get_page_links(url):
    base_url = "http://www.drinksmixer.com"
    soup = BeautifulSoup(urllib2.urlopen(url).read())
    links = [base_url + l['href'] for l in soup('a', href=re.compile("^/desc"))]
    return links
    
