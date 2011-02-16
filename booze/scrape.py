from BeautifulSoup import BeautifulSoup
from booze.models import DrinkLink

import urllib2
import re

BASE_URL = 'http://www.drinksmixer.com'

def get_drink_links():
    for num in range(1, 125):
        url = 'http://www.drinksmixer.com/cat/1/%d/' % num
        soup = BeautifulSoup(urllib2.urlopen(url).read())
        parse_drink_links(soup)


def parse_drink_links(soup):
    drinklinks = [link for link in soup('div', {'class':'clr'})[0]('a', href=re.compile(r"^/drink"))]
    for link in drinklinks:
        href = BASE_URL + link['href']
        name = link.renderContents()
        print "Saving %s at %s" % (name, href)
        DrinkLink.objects.get_or_create(href=href, name=name)
