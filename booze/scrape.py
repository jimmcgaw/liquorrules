from BeautifulSoup import BeautifulSoup
from booze.models import DrinkLink, Cocktail, Ingredient

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


