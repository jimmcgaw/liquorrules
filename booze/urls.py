from django.conf.urls.defaults import *

urlpatterns = patterns('booze.views',
    (r'^$', 'home', 
        {'template_name': 'booze/home.html' }, 'booze_home'),
)
