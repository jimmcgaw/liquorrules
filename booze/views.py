from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext

from booze.models import Cocktail

def home(request, template_name="booze/home.html"):
    q = u''
    if request.method == 'POST':
        q = request.POST.get('q', u'')
        page = request.POST.get('page', 1)
        drinks, paginator = Cocktail.objects.search(q, page)
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))